"use strict";document.querySelectorAll("[data-text-color]").forEach((t=>{const r=function(t){let r=0;for(let e=0;e<t.length;e++)r=t.charCodeAt(e)+((r<<5)-r);let e="#";for(let t=0;t<3;t++)e+=("00"+(r>>8*t&255).toString(16)).substr(-2);return e}(t.dataset.textColor);t.style.color=r,t.style.backgroundColor=function(t){if(0===t.indexOf("#")&&(t=t.slice(1)),3===t.length&&(t=t[0]+t[0]+t[1]+t[1]+t[2]+t[2]),6!==t.length)throw new Error("Invalid HEX color.");var r=(255-parseInt(t.slice(0,2),16)).toString(16),e=(255-parseInt(t.slice(2,4),16)).toString(16),o=(255-parseInt(t.slice(4,6),16)).toString(16);return"#"+r.padStart(2,"0")+e.padStart(2,"0")+o.padStart(2,"0")}(r)}));
//# sourceMappingURL=index.js.map