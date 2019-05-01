import Vue from 'vue';

let requestActive = false,
    requestQueue = [],
    hasOnlineEventListener = false;

const doRequest = (url, settings) => {
    settings = settings || {};
    if (typeof url === 'object')
        settings = url;
    else
        settings.url = url;

    if (navigator.onLine && !requestActive) {
        requestActive = true;
        return $.ajax(settings)
        .always(() => {
            requestActive = false;
            if (requestQueue.length)
                doRequest(requestQueue.shift());
        })
        .fail(jqXHR => {
            // Don't flash error if suppressError or polling
            if (settings.suppressError !== true && !settings.polling)
                flashError(jqXHR);
        });
    }
    else {
        if (!navigator.onLine && !hasOnlineEventListener) {
            window.addEventListener('online', ()=> {
                if (requestQueue.length)
                    doRequest(requestQueue.shift());
            });
            hasOnlineEventListener = true;
        }
        if (!settings.polling) {
            requestQueue.push(settings);
        }
    }
}

const eventBus = new Vue();

const flashMessage = (content, options) => {
    options = options || {};
    options.content = content;
    eventBus.$emit('flash::display', options);
}

const flashError = jqXHR => {
    let msg = '';
    if (jqXHR.getResponseHeader('content-type') === "application/json" && typeof(jqXHR.responseText) == 'string') {
        var parsed = $.parseJSON(jqXHR.responseText);
        if (parsed.title)
            msg = '<h4>' + parsed.title + '</h4>';
        if (parsed.body && parsed.body != parsed.title) {
            msg += parsed.body;
        } else if (parsed.message && parsed.message != parsed.title) {
            msg += parsed.message;
        } else if (parsed.msg) {
            msg += parsed.msg;
        }
    } else {
        msg = '<h4>' + jqXHR.status + ' ' + jqXHR.statusText + '</h4>' + jqXHR.responseText
    }
    flashMessage(msg, {type: 'danger'});
}

export {
    eventBus,
    flashError,
    flashMessage,
    doRequest
}
