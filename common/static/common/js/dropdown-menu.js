/* global $ */

class DropdownMenus {
  constructor() {

    var self = this;
    window.shown_dropdown = null; // currently shown menu (null if none). Make it global (not clean but works)

    // click on first level menu (the one to drop DOWN)
    $("ul.dropdown > li").click(function(ev) {

      if (window.shown_dropdown) {
        // console.log("menu", this, ev);
        if ((ev.target.tagName !== 'SELECT') && (ev.target.tagName !== 'INPUT')) {
          self.hide_all();
        }
      } else {
        var dropdown = $('ul:first', this);
        if (dropdown.length > 0) {
            dropdown.css('max-height', '1000px');
            dropdown.css('border-width', '1px');
            window.shown_dropdown = dropdown.get(0);
            //console.debug("shown_dropdown:", self.shown_dropdown);
            ev.stopPropagation();
        }
      }

    // Comme on a pas stoppé la propagation, l'event va "bubbler", la callback sur le 'body' va être appelée et le menu sera caché.
    });

    $('html').click(function(e){
        //console.debug("click body");

        // Ne pas fermer le menu si on clique sur un de ses enfants
        //console.debug("shown_dropdown:", self.shown_dropdown);
        if (window.shown_dropdown && (!window.shown_dropdown.contains(e.target)))
         {
          window.shown_dropdown.style['max-height']= 0;
          window.shown_dropdown.style['border-width']= 0;
          window.shown_dropdown = null;
         }
        });
  }

  hide_all() {
      if (window.shown_dropdown) {
          window.shown_dropdown.style['max-height']= 0;
          window.shown_dropdown.style['border-width']= 0;
          //window.shown_dropdown.css('max-height', '0');
          //window.shown_dropdown.css('border-width', '0');
          window.shown_dropdown = null;
      }
  }
}
