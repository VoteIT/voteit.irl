import Vue from 'vue';

/*
 *  Requests class makes sure requests done with each instance is performed serially.
 *  If there is an ongoing request, new requests will be queued.
 *  
 *  Methods:
 *      get(url[, settings]) -- Perform HTTP GET.
 *      post(url, data[, settings]) -- Perform HTTP POST.
 *
 *  Settings:
 *      polling: Boolean -- Will not be queued and not performed if document is hidden.
 *      suppressError: Boolean -- Will not flash error message on request failure.
 */
class Requests {
    constructor() {
        this.requestActive = false;
        this.requestQueue = [];
    }

    next() {
        if (this.requestQueue.length && !this.requestActive)
            this.request(this.requestQueue.shift());
    }

    request(url, settings) {
        settings = settings || {};
        if (typeof url === 'object')
            settings = url;
        else
            settings.url = url;

        if (this.requestActive) {
            settings.deferred = $.Deferred();
            if (!settings.polling)
                this.requestQueue.push(settings);
            return settings.deferred;
        }
        else {
            this.requestActive = true;
            return $.ajax(settings)
            .done((data, textStatus, jqXHR) => {
                if (settings.deferred)
                    settings.deferred.resolve(data, textStatus, jqXHR);
            })
            .fail((jqXHR, textStatus, errorThrown) => {
                // Don't flash error if suppressError or polling
                if (settings.suppressError !== true && !settings.polling)
                    flashError(jqXHR);
                if (settings.deferred)
                    settings.deferred.reject(jqXHR, textStatus, errorThrown);
            })
            .always(() => {
                this.requestActive = false;
                this.next();
            })
        }
    }

    get(url, settings) {
        settings = settings || {};
        return this.request(url, settings);
    }

    post(url, data, settings) {
        settings = settings || {};
        settings.method = 'POST';
        settings.data = data;
        return this.request(url, settings);
    }
}

/*
 * Polling class. Instantiate with a Requests() instance.
 *
 * Methods:
 * addService(url[, intervalTime, callback])
 * clearService(url)
 */
class Polling {
    constructor(requests) {
        this.requests = requests;
        this.services = [];
        this.intervalDefault = 5000;  // msec
        window.addEventListener('online', this._startAll.bind(this));
        window.addEventListener('offline', this._stopAll.bind(this));
        if (document.hidden !== undefined) {
            document.addEventListener('visibilitychange', () => {
                if (document.hidden)
                    this._stopAll()
                else
                    this._startAll()
            });
        }
    }

    _startService(service) {
        const serviceCaller = () => {
            const request = this.requests.get(service.url, { polling: true });
            if (service.callback)
                request.done(service.callback);
        }
        serviceCaller();
        if (service.intervalId === undefined) {
            service.intervalId = setInterval(serviceCaller, service.intervalTime);
        }
    }

    _stopService(service) {
        if (service.intervalId) {
            clearInterval(service.intervalId);
            delete service.intervalId;
        }
    }

    _startAll() {
        this.services.forEach(service => {
            this._startService(service);
        });
    }

    _stopAll() {
        this.services.forEach(service => {
            this._stopService(service);
        });
    }

    addService(url, intervalTime, callback) {
        intervalTime = intervalTime || this.intervalDefault;
        const service = { url, intervalTime, callback };
        this.services.push(service);
        this._startService(service);
    }

    clearService(url) {
        this.services.filter(s => s.url === url).forEach(service => {
            this._stopService(service);
        });
        this.services = this.services.filter(s => s.url !== url);
    }
}

const requests = new Requests();
const polling = new Polling(requests);
const eventBus = new Vue();

const flashMessage = (content, options) => {
    options = options || {};
    options.content = content;
    eventBus.$emit('flash::display', options);
}

const modal = {
    // Open has two signatures.
    // Call with (href, params) or (params).
    open(href, params) {
        if (typeof href === 'object')
            params = href;
        else {
            params = params || {};
            params.href = href;
        }
        eventBus.$emit('modal::open', params);
    },
    close() {
        eventBus.$emit('modal::close');
    }
};

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
    requests,
    polling,
    modal
}
