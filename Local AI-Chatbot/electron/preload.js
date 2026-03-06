/**
 * Electron Preload Script
 * Safely exposes APIs from the main process to the renderer process
 */

const { contextBridge, ipcRenderer } = require('electron');

// Expose protected methods that allow the renderer process to use
// ipcRenderer without exposing the entire object
contextBridge.exposeInMainWorld('electronAPI', {
    // Get list of available models
    getModels: () => ipcRenderer.invoke('get-models'),

    // Set the active model
    setModel: (modelName) => ipcRenderer.invoke('set-model', modelName),

    // Download a new model
    downloadModel: (modelName) => ipcRenderer.invoke('download-model', modelName),

    // Check if running in Electron
    isElectron: true
});

console.log('Preload script loaded successfully');
