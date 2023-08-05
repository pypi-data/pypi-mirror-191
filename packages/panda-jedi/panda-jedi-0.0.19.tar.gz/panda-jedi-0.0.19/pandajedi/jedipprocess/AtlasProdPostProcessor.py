import re
import sys

from six import iteritems

from .PostProcessorBase import PostProcessorBase
from . import AtlasPostProcessorUtils

from pandaserver.dataservice import DataServiceUtils
from pandaserver.taskbuffer import EventServiceUtils


# post processor for ATLAS production
class AtlasProdPostProcessor (PostProcessorBase):

    # constructor
    def __init__(self,taskBufferIF,ddmIF):
        PostProcessorBase.__init__(self,taskBufferIF,ddmIF)


    # main
    def doPostProcess(self,taskSpec,tmpLog):
        # pre-check
        try:
            tmpStat = self.doPreCheck(taskSpec,tmpLog)
            if tmpStat:
                return self.SC_SUCCEEDED
        except Exception:
            errtype,errvalue = sys.exc_info()[:2]
            tmpLog.error('doPreCheck failed with {0}:{1}'.format(errtype.__name__,errvalue))
            return self.SC_FATAL
        # get DDM I/F
        ddmIF = self.ddmIF.getInterface(taskSpec.vo)
        # loop over all datasets
        for datasetSpec in taskSpec.datasetSpecList:
            # skip pseudo output datasets
            if datasetSpec.type in ['output'] and datasetSpec.isPseudo():
                continue
            try:
                # remove wrong files
                if datasetSpec.type in ['output']:
                    # get successful files
                    okFiles = self.taskBufferIF.getSuccessfulFiles_JEDI(datasetSpec.jediTaskID,datasetSpec.datasetID)
                    if okFiles is None:
                        tmpLog.warning('failed to get successful files for {0}'.format(datasetSpec.datasetName))
                        return self.SC_FAILED
                    # get files in dataset
                    ddmFiles = ddmIF.getFilesInDataset(datasetSpec.datasetName,skipDuplicate=False,ignoreUnknown=True)
                    tmpLog.debug('datasetID={0}:Name={1} has {2} files in DB, {3} files in DDM'.format(datasetSpec.datasetID,
                                                                                                      datasetSpec.datasetName,
                                                                                                      len(okFiles),len(ddmFiles)))
                    # check all files
                    toDelete = []
                    for tmpGUID,attMap in iteritems(ddmFiles):
                        if attMap['lfn'] not in okFiles:
                            did = {'scope':attMap['scope'], 'name':attMap['lfn']}
                            toDelete.append(did)
                            tmpLog.debug('delete {0} from {1}'.format(attMap['lfn'],datasetSpec.datasetName))
                    # delete
                    if toDelete != []:
                        ddmIF.deleteFilesFromDataset(datasetSpec.datasetName,toDelete)
            except Exception:
                errtype,errvalue = sys.exc_info()[:2]
                tmpLog.warning('failed to remove wrong files with {0}:{1}'.format(errtype.__name__,errvalue))
                return self.SC_FAILED
            try:
                # freeze output and log datasets
                if datasetSpec.type in ['output','log','trn_log']:
                    tmpLog.info('freezing datasetID={0}:Name={1}'.format(datasetSpec.datasetID,datasetSpec.datasetName))
                    ddmIF.freezeDataset(datasetSpec.datasetName,ignoreUnknown=True)
            except Exception:
                errtype,errvalue = sys.exc_info()[:2]
                tmpLog.warning('failed to freeze datasets with {0}:{1}'.format(errtype.__name__,errvalue))
                return self.SC_FAILED
            try:
                # delete transient datasets
                if datasetSpec.type in ['trn_output']:
                    tmpLog.debug('deleting datasetID={0}:Name={1}'.format(datasetSpec.datasetID,datasetSpec.datasetName))
                    retStr = ddmIF.deleteDataset(datasetSpec.datasetName,False,ignoreUnknown=True)
                    tmpLog.info(retStr)
            except Exception:
                errtype,errvalue = sys.exc_info()[:2]
                tmpLog.warning('failed to delete datasets with {0}:{1}'.format(errtype.__name__,errvalue))
        # check duplication
        if self.getFinalTaskStatus(taskSpec) in ['finished','done'] and taskSpec.gshare != 'Test':
            nDup = self.taskBufferIF.checkDuplication_JEDI(taskSpec.jediTaskID)
            tmpLog.debug('checked duplication with {0}'.format(nDup))
            if nDup > 0:
                errStr = 'paused since {0} duplication found'.format(nDup)
                taskSpec.oldStatus = self.getFinalTaskStatus(taskSpec)
                taskSpec.status = 'paused'
                taskSpec.setErrDiag(errStr)
                tmpLog.debug(errStr)
        # delete ES datasets
        if taskSpec.registerEsFiles():
            try:
                targetName = EventServiceUtils.getEsDatasetName(taskSpec.jediTaskID)
                tmpLog.debug('deleting ES dataset name={0}'.format(targetName))
                retStr = ddmIF.deleteDataset(targetName,False,ignoreUnknown=True)
                tmpLog.debug(retStr)
            except Exception:
                errtype,errvalue = sys.exc_info()[:2]
                tmpLog.warning('failed to delete ES dataset with {0}:{1}'.format(errtype.__name__,errvalue))
        try:
            AtlasPostProcessorUtils.send_notification(self.taskBufferIF, ddmIF, taskSpec, tmpLog)
        except Exception as e:
            tmpLog.error('failed to talk to external system with {0}'.format(str(e)))
            return self.SC_FAILED
        try:
            self.doBasicPostProcess(taskSpec,tmpLog)
        except Exception:
            errtype,errvalue = sys.exc_info()[:2]
            tmpLog.error('doBasicPostProcess failed with {0}:{1}'.format(errtype.__name__,errvalue))
            return self.SC_FATAL
        return self.SC_SUCCEEDED



    # final procedure
    def doFinalProcedure(self,taskSpec,tmpLog):
        tmpLog.info('final procedure for status={0} processingType={1}'.format(taskSpec.status,
                                                                               taskSpec.processingType))
        if taskSpec.status in ['done','finished'] or \
                (taskSpec.status == 'paused' and taskSpec.oldStatus in ['done','finished']):
            trnLifeTime = 14*24*60*60
            trnLifeTimeMerge = 40*24*60*60
            ddmIF = self.ddmIF.getInterface(taskSpec.vo)
            # set lifetime to transient datasets
            metaData = {'lifetime':trnLifeTime}
            datasetTypeListI = set()
            datasetTypeListO = set()
            for datasetSpec in taskSpec.datasetSpecList:
                if datasetSpec.type in ['log','output']:
                    if datasetSpec.getTransient() is True:
                        tmpLog.debug('set metadata={0} to datasetID={1}:Name={2}'.format(str(metaData),
                                                                                        datasetSpec.datasetID,
                                                                                        datasetSpec.datasetName))
                        for metadataName,metadaValue in iteritems(metaData):
                            ddmIF.setDatasetMetadata(datasetSpec.datasetName,metadataName,metadaValue)
                # collect dataset types
                datasetType = DataServiceUtils.getDatasetType(datasetSpec.datasetName)
                if datasetType not in ['',None]:
                    if datasetSpec.type == 'input':
                        datasetTypeListI.add(datasetType)
                    elif datasetSpec.type == 'output':
                        datasetTypeListO.add(datasetType)
            # set lifetime to parent transient datasets
            if taskSpec.processingType in ['merge'] and \
                    (taskSpec.status == 'done' or \
                         (taskSpec.status == 'finished' and self.getFinalTaskStatus(taskSpec, checkParent=False) == 'done') or \
                         (taskSpec.status == 'paused' and \
                              (taskSpec.oldStatus == 'done' or \
                                   (taskSpec.oldStatus == 'finished' and self.getFinalTaskStatus(taskSpec, checkParent=False) == 'done')))):
                # get parent task
                if taskSpec.parent_tid not in [None,taskSpec.jediTaskID]:
                    # get parent
                    tmpStat,parentTaskSpec = self.taskBufferIF.getTaskDatasetsWithID_JEDI(taskSpec.parent_tid,None,False)
                    if tmpStat and parentTaskSpec is not None:
                        # set lifetime to parent datasets if they are transient
                        for datasetSpec in parentTaskSpec.datasetSpecList:
                            if datasetSpec.type in ['output']:
                                # check dataset type
                                datasetType = DataServiceUtils.getDatasetType(datasetSpec.datasetName)
                                if datasetType not in datasetTypeListI or datasetType not in datasetTypeListO:
                                    continue
                                metaData = {'lifetime': trnLifeTimeMerge}
                                tmpMetadata = ddmIF.getDatasetMetaData(datasetSpec.datasetName)
                                if tmpMetadata['transient'] is True:
                                    tmpLog.debug('set metadata={0} to parent jediTaskID={1}:datasetID={2}:Name={3}'.format(str(metaData),
                                                                                                                          taskSpec.parent_tid,
                                                                                                                          datasetSpec.datasetID,
                                                                                                                          datasetSpec.datasetName))
                                    for metadataName,metadaValue in iteritems(metaData):
                                        ddmIF.setDatasetMetadata(datasetSpec.datasetName,metadataName,metadaValue)
        # set lifetime to failed datasets
        if taskSpec.status in ['failed','broken','aborted']:
            trnLifeTime = 30*24*60*60
            ddmIF = self.ddmIF.getInterface(taskSpec.vo)
            # only log datasets
            metaData = {'lifetime':trnLifeTime}
            for datasetSpec in taskSpec.datasetSpecList:
                if datasetSpec.type in ['log']:
                    tmpLog.debug('set metadata={0} to failed datasetID={1}:Name={2}'.format(str(metaData),
                                                                                           datasetSpec.datasetID,
                                                                                           datasetSpec.datasetName))
                    for metadataName,metadaValue in iteritems(metaData):
                        ddmIF.setDatasetMetadata(datasetSpec.datasetName,metadataName,metadaValue)
        return self.SC_SUCCEEDED
