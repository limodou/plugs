/**************************************************
 * browser desktop notification api js lib
 * Author limodou@gmail.com
 * License MIT
 * version 0.1
 *
 * Inspired by https://github.com/gotardo/HTML5-Desktop-Notif
 **************************************************/
var Notify = {
    icon : null,
    title : null, 
    message: null,
    
    // Behavior Config. params
    autoclose           : null,

    isSupported : function () {
        return window.webkitNotifications;
    },

    log: function(){
        if (window.console && console.log){
            var args = Array.prototype.slice.call(arguments);
            console.log.apply(console, args);
        }
    },
    request: function(){
        var notify = this.isSupported();
        if (notify.checkPermission() == 1)
            notify.requestPermission();                     
    },
    check: function(){
        var notify = this.isSupported();
        return notify.checkPermission();
    },
    /* ------------------------------------------
        Shows the notification (if possible)
        message = {
            icon:
            title:
            message:
            ondisplay:
            onclick:
            onerror:
            onclose:
        }
    ------------------------------------------ */       

    show    : function (message) {
        var opts = {
            icon: message.icon || this.icon,
            title: message.title || this.title,
            message: message.message || this.message,
            ondisplay: message.ondisplay || function(){},
            onclick: message.onclick || function(){},
            onerror: message.onerror || function(){},
            onclose: message.onclose || function(){}
        };
        
        this.log('test');
        var notify = this.isSupported();
        //If webkitNotifications object is not available and we are in debug mode, an exception will be thrown...
        if (!notify) {
            return;
        }   
        else {
            //Check for permission to show notifications. Request permission if notifications are not allowed
            this.request();
            if (notify.checkPermission() == 2) {
                this.log("Permission are denied!!" + notify.checkPermission());
            }
            //If permission is allowed, the notification is shown.

            if (notify.checkPermission() == 0) {
                var n = notify.createNotification(opts.icon, opts.title, opts.message);     
                n.ondisplay = opts.ondisplay;
                n.onclick = opts.onclick;
                n.onerror = opts.onerror;
                n.onclose = opts.onclose;

                n.show();

                if (this.autoclose) 
                    setTimeout(function () {
                        Notif.wkNotif.cancel();
                    }, this.autoclose * 1000);                      
            }
        }//End If

        return this;
    }

};
