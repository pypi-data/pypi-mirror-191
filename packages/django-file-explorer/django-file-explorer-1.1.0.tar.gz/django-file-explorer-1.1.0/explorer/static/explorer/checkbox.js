const selected_idx = [];

function _getCheckboxNumberFromID(check_box_id){
    const break_id = check_box_id.split('_');
    let idx = Number(break_id[break_id.length - 1]);
    return idx;
}

function _addSelectedIdx(idx){
    // GETTING ARRAY INDEX
    let array_index = selected_idx.indexOf(idx);

    // IF INDEX NOT EXISTS
    if (array_index == -1){
        selected_idx.push(idx);
    }
}

function _removeSelectedIdx(idx){
    // GETTING ARRAY INDEX
    let array_index = selected_idx.indexOf(idx);

    // IF INDEX NOT EXISTS
    if (array_index != -1){
        selected_idx.splice(array_index, 1);
    }
}

function _updateStatusOfSelectAllCheckbox(){
    // GETTING INFORMATION
    let checkboxes = document.getElementsByName('file_checkbox');
    let state = document.getElementById('select_all_check');

    // MAKING CONDITION
    if (checkboxes.length == selected_idx.length){
        state.checked = true;
    }else {
        state.checked = false;
    }
}

function selectAllCheckbox(){
    // GETTING INFORMATION
    let state = document.getElementById('select_all_check').checked;
    let checkboxes = document.getElementsByName('file_checkbox');

    // CHECKING AND DISCHECKING ALL CHECKBOX
    for (let checkbox of checkboxes){
        // GETTING CHECKBOX IDX
        let check_box_id = checkbox.id;
        let idx = _getCheckboxNumberFromID(check_box_id);

        // MAKING ADDING LOGIC
        if (state == true){
            checkbox.checked = true;
            _addSelectedIdx(idx);
        }
        else {
            checkbox.checked = false;
            _removeSelectedIdx(idx);
        }
    }

    // UPDATING ACTION BUTTON STATUS
    updateActionBtnStatus();
}

// GETTING SELECTED ARAY
function registerCheckbox(check_box_id){
    // GETTING NUMBER FROM THE ID
    let idx = _getCheckboxNumberFromID(check_box_id);

    // GETTING CHECKED STATUS
    let status = document.getElementById(check_box_id).checked;

    // IMPLIMENTING CONDITION
    if (status){
        _addSelectedIdx(idx);
    } else {
        _removeSelectedIdx(idx);
    }

    // UPDATING ACTION BUTTON STATUS
    updateActionBtnStatus();

    // UPDATING STATUS OF SELECT ALL CHECKBOX
    _updateStatusOfSelectAllCheckbox()
}

function updateActionBtnStatus() {
    if (selected_idx.length != 0) {
        enableAllActionBtn();
    } else {
        diableAllActionBtn();
    }
}