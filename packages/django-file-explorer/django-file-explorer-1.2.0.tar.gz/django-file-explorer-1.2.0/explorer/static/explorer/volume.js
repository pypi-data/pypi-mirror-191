
function getVolumeSelectClass(vol_name){
    // LOADING VOLUME DATA
    const volume_data = JSON.parse(document.getElementById('volume_data').textContent);

    // LOOPING THROUGH EACH VOLUME
    let selected = 'deactive';
    for (let volume of volume_data){
        if (volume.name == vol_name){
            if (volume.selected){
                selected = 'active';
            }
        }
    }
    return selected;
}

function getVolumeEnableClass(vol_name){
    // LOADING VOLUME DATA
    const volume_data = JSON.parse(document.getElementById('volume_data').textContent);

    // LOOPING THROUGH EACH VOLUME
    let status = 'disabled';
    for (let volume of volume_data){
        if (volume.name == vol_name){
            if (volume.error == null){
                status = 'enable';
            }
        }
    }
    return status;
}

function getTitleInfo(vol_name){
    // LOADING VOLUME DATA
    const volume_data = JSON.parse(document.getElementById('volume_data').textContent);

    // LOOPING THROUGH EACH VOLUME
    let status = '';
    for (let volume of volume_data){
        if (volume.name == vol_name){
            if (volume.error == null){
                status = 'Active volume';
            }else {
                status = volume.error;
            }
        }
    }
    return status;
}

function getSelectedVolume(){
    // LOADING VOLUME DATA
    const volume_data = JSON.parse(document.getElementById('volume_data').textContent);

    // LOOPING THROUGH EACH VOLUME
    let vol_name = '';
    for (let volume of volume_data){
        if (volume.selected){
            vol_name = volume.name;
        }
    }
    return vol_name;
}