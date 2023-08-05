from __future__ import annotations as _annotations
from abc import ABC, abstractmethod
from SimpleWorkspace.Utility import Console as _ConsoleUtility
import os as _os
import json as _json
import SimpleWorkspace as _sw
from copy import deepcopy

class SettingsManager_Base(ABC):
    Settings = {}
    _cached_DefaultSettings = {}
    def __init__(self, settingsPath):
        self._settingsPath = settingsPath
        self._CacheDefaultSettings()

    def _CacheDefaultSettings(self):
        self._cached_DefaultSettings = deepcopy(self.Settings)

    @abstractmethod
    def _ParseSettingsFile(self, filepath) -> dict:
        '''responsible for parsing setting file and returning a settings object'''
    @abstractmethod
    def _ExportSettingsFile(self, settingsObject, outputPath):
        '''responsible for saving the settingsObject to file location in self._settingsPath'''
  
    def ClearSettings(self):
        self.Settings = deepcopy(self._cached_DefaultSettings)

    def LoadSettings(self):
        '''Loads the setting file from specified location to the memory at self.settings'''
        self.ClearSettings()
        if not (_os.path.exists(self._settingsPath)):
            return

        settingsObject = self._ParseSettingsFile(self._settingsPath)
        #instead of replacing all the settings, we set it to default state, and copy over keys
        #incase default settings are specified/overriden, even if only one of the default setting existed in the file
        #we will keep other default settings as specified and only change value of new settings parsed
        self.Settings.update(settingsObject) 
        return

    def SaveSettings(self):
        self._ExportSettingsFile(self.Settings, self._settingsPath)


class SettingsManager_JSON(SettingsManager_Base):
    def _ParseSettingsFile(self, filepath):
        return _json.loads(_sw.IO.File.Read(filepath))

    def _ExportSettingsFile(self, settingsObject, outputPath):
        jsonData = _json.dumps(settingsObject)
        _sw.IO.File.Create(outputPath, jsonData)
        return


class SettingsManager_AutoMapped_JSON(ABC):
    '''
    SettingsManager class that helps with accessing settings file in an abstract and simplified way.
    All derived classes automatically implement automapper of typed settings, where properties starting with "Setting_XXX"
    will automatically be loaded/exported.
    '''
    _cached_DefaultSettings = {}

    def __init__(self, settingsPath):
        self._settingsPath = settingsPath
        self._CacheDefaultSettings()

    def _CacheDefaultSettings(self):
        settingsObject = self._ExportTypedSettings()
        self._cached_DefaultSettings = deepcopy(settingsObject)

    def _ParseSettingsFile(self, filepath):
        '''responsible for parsing setting file and returning a settings object'''
        return _json.loads(_sw.IO.File.Read(filepath))

    def _ExportSettingsFile(self, settingsObject, outputPath):
        '''responsible for saving the settingsObject to file location in self._settingsPath'''
        jsonData = _json.dumps(settingsObject)
        _sw.IO.File.Create(outputPath, jsonData)

    _cached_GetTypedSettingPropNames = None
    def _GetTypedSettingPropNames(self):
        '''returns dictionary of key = propertyNames of typedSettings, and the value consists of the settingName aka without "Setting_" prefix'''
        if(self._cached_GetTypedSettingPropNames is not None):
            return self._cached_GetTypedSettingPropNames
        
        allTypedProperties = {}
        classReflector = vars(self.__class__)
        for propertyName, value in classReflector.items():
            if (propertyName.startswith("Setting_")) and (not callable(value)):
                allTypedProperties[propertyName] = propertyName.removeprefix("Setting_")

        self._cached_GetTypedSettingPropNames = allTypedProperties
        return self._cached_GetTypedSettingPropNames

    def _MapTypedSettings(self, settingsObject: dict):
        '''Is an automapper by default for all Settings_xxx variables(Case Sensitive!), you may override this if you want to map specific logic'''
        allTypedProperties = self._GetTypedSettingPropNames()

        for key, value in settingsObject.items():
            propertyName = "Setting_" + key
            if (propertyName in allTypedProperties):
                setattr(self, propertyName, value)
        return
    
    def _ExportTypedSettings(self):
        '''Maps all the typed variables to settingsObject to prepare for exporting the file'''
        settingsObject = {}
        allTypedProperties = self._GetTypedSettingPropNames()
        for propertyName, settingName in allTypedProperties.items():
            settingsObject[settingName] = getattr(self, propertyName)
        return settingsObject

    def ClearSettings(self):
        self._MapTypedSettings(deepcopy(self._cached_DefaultSettings))

    def LoadSettings(self):
        '''Loads the setting file from specified location to the memory at self.settings'''
        self.ClearSettings()
        if not (_os.path.exists(self._settingsPath)):
            return

        settingsObject = self._ParseSettingsFile(self._settingsPath)
        self._MapTypedSettings(settingsObject)
        return

    def SaveSettings(self):
        settingsObject = self._ExportTypedSettings()
        self._ExportSettingsFile(settingsObject, self._settingsPath)




# class SettingsManagerExample(SettingsManager_AutoMapped_JSON):
#     Setting_autorun = 1
#     Setting_testString = "hej"

# settingsManager = SettingsManagerExample("./test1.txt")
# settingsManager.LoadSettings()
# settingsManager.Setting_autorun = 5
# settingsManager.SaveSettings()