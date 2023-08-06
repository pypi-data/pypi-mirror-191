window.onload = function() {
    correctActionBtn();
    correctVolumeList();
};

function correctVolumeList(){
    // GETTING VOLUME LIST
    let vol_list = document.getElementsByName('volume-list');

    // LOOPING THROUGH EACH VOLUME
    for (let vol of vol_list){        
        // GETTING SELETECTED CLASS
        selected = getVolumeSelectClass(vol.id);

        // GETTING ENABLE CLASS
        enable = getVolumeEnableClass(vol.id);

        // GETTING TITLE INFO
        title = getTitleInfo(vol.id)

        // UPDATING CLASS
        vol.className += ` ${selected} ${enable}`;
        
        // UPDATING TITLE
        vol.title = title;
    }
}

function correctActionBtn(){
    // GETTING LIST OF ALL BUTTON
    let action_btn = document.getElementsByName('action-btn');

    for (let btn of action_btn){
        // GETING ACTION NAME
        action = btn.id;

        // CHAINING TEXT
        let action_str = capitalizeFirstLetter(action);
        btn.innerHTML = action_str;

        // CHAINING COLOR
        btn_detail = action_btn_detail[action];
        if (btn_detail != undefined){
            btn.className += ` ${btn_detail['color']}`;
            btn.title = `${action_str} data`;
            btn.disabled = btn_detail['disabled'];
        }else {
            btn.title = 'Action color not defined';
        }
    }
}