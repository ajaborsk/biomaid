var smart_view_checkbox_fmt = function(cell, formatterParams, onRendered) {
    "use strict";
    if (cell._cell.value === true) {
        return "<i class=\"fa-regular fa-circle-check\"></i>";
    }
    else if (cell._cell.value === false) {
        return "<i class=\"fa-regular fa-circle-xmark\"></i>";
    }
    else {
        return "<i class=\"fa-regular fa-circle\"></i>";
    }
};
