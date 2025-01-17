Tabulator.extendModule("format", "formatters", {
  suivi: function(cell, formatterParams, onRendered) {
    var s = cell.getValue();
    if (s)
     {
      s = s.substring(0,2);
      //console.log("s=", s);
      if (s=="0-") {
        cell.getElement().style.backgroundColor = '#aaa';
      } else if (s=="1-") {
        cell.getElement().style.backgroundColor = '#afa';
      } else if (s=='2-') {
        cell.getElement().style.backgroundColor = '#abf';
      } else if (s=='3-') {
        cell.getElement().style.backgroundColor = '#ffa';
      } else if (s=='4-') {
        cell.getElement().style.backgroundColor = '#faa';
      } else {
        cell.getElement().style.backgroundColor = null;
      }
    }
    return cell.getValue();
  },
  suivi_commande: function(cell, formatterParams, onRendered) {
    var s = cell.getValue();
    if (s)
     {
      sb = s.substring(0,2);
      //console.log("s=", s);
      if (sb=="0-") {
        cell.getElement().style.backgroundColor = '#aaa';
      } else if (sb=="1-") {
        cell.getElement().style.backgroundColor = '#afa';
      } else if (sb=='2-') {
        cell.getElement().style.backgroundColor = '#abf';
      } else if (sb=='3-') {
        cell.getElement().style.backgroundColor = '#ffa';
      } else if (sb=='4-') {
        cell.getElement().style.backgroundColor = '#faa';
      } else if (/[A-Za-z0-9][A-Za-z0-9]\d\d\d\d\d\d/.test(s)) {
        // On arrive ici si le contenu de la cellule contient un numéro de commande
        cell.getElement().style.backgroundColor = '#afa';
      } else if (/DRA\d\d\d\d-\d\d\d\d/.test(s)) {
        // On arrive ici si le contenu de la cellule contient un numéro de DRA
        cell.getElement().style.backgroundColor = '#abf';
      } else {
        cell.getElement().style.backgroundColor = null;
      }
    }
    return cell.getValue();
  },
  suivi_couleur: function(cell, formatterParams, onRendered) {
    var s = cell.getValue();
    var content = "";
    if (s)
     {
      s = s.substring(0,2);
      //console.log("s=", s);
      if (s=="0-") {
        cell.getElement().style.backgroundColor = '#aaa';
        content = "N/A";
      } else if (s=="1-") {
        cell.getElement().style.backgroundColor = '#afa';
        content = "Terminé";
      } else if (s=='2-') {
        cell.getElement().style.backgroundColor = '#abf';
        content = "En cours";
      } else if (s=='3-') {
        cell.getElement().style.backgroundColor = '#ffa';
        content = "En attente";
      } else if (s=='4-') {
        cell.getElement().style.backgroundColor = '#faa';
        content = "Bloqué";
      } else {
        cell.getElement().style.backgroundColor = null;
      }
    }
    return content;
  },
  suivi_commande_couleur: function(cell, formatterParams, onRendered) {
    var s = cell.getValue();
    var content = "";
    if (s)
     {
      sb = s.substring(0,2);
      //console.log("s=", s);
      if (sb=="0-") {
        cell.getElement().style.backgroundColor = '#aaa';
        content = "N/A";
      } else if (sb=="1-") {
        // On arrive ici aussi si le contenu de la cellule contient un numéro de commande
        cell.getElement().style.backgroundColor = '#afa';
        content = "Terminé";
      } else if (sb=='2-') {
        cell.getElement().style.backgroundColor = '#abf';
        content = "En cours";
      } else if (sb=='3-') {
        cell.getElement().style.backgroundColor = '#ffa';
        content = "En attente";
      } else if (sb=='4-') {
        cell.getElement().style.backgroundColor = '#faa';
        content = "Bloqué";
      } else {
        var all_bc = [...s.matchAll(/[A-Za-z0-9][A-Za-z0-9]\d\d\d\d\d\d/g)];
        if (all_bc.length > 0) {
          // On arrive ici aussi si le contenu de la cellule contient un numéro de commande
          cell.getElement().style.backgroundColor = '#afa';
          content = "Terminé";
          for (var i=0;i<all_bc.length;i++) {
            content += "\n" + all_bc[i][0];
          }
        } else if (/DRA\d\d\d\d-\d\d\d\d/.test(s)) {
          cell.getElement().style.backgroundColor = '#abf';
          content = "En cours";
        } else {
          cell.getElement().style.backgroundColor = null;
        }
      }
    }
    return content;
  },
});