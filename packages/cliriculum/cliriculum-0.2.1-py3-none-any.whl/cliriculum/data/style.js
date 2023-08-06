function styleContact() {
    const profile = document.getElementById("profile_pic");
    var contact = document.getElementById("contact");
    // Override padding-top of contact box
    if (profile) {
        // margintop = getComputedStyle(document.body).getPropertyValue("--pagedjs-margin-top") // a string
        contact.style.setProperty("padding-top", "calc(var(--pagedjs-margin-top) / 2)");
    } else {
      var p_1 = contact.querySelector("p");  // traverse tree subset
      p_1.style.setProperty('margin-top', '0');
    }
};

class StyleContact extends Paged.Handler {
    constructor(chunker, polisher, caller) {
        super(chunker, polisher, caller);
    }
    afterPreview(pages) {
        styleContact();
    }
}
// window.addEventListener("load", styleContact); // does not work because of pagedjs recomputing parts of dom.
// For this reason I use a hook.

Paged.registerHandlers(StyleContact);
