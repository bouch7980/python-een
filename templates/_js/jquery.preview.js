(function($) {

    $.fn.cameraPreview = function(options) {

        // use the defaults or customized options if they exist
        var options     =   options || {},
            camera_id   =   options.camera_id || '',
            width       =   options.width || 320,
            height      =   options.height || 180,
            delay       =   options.delay || 1000
            preview     =   new Image(),
            buffer      =   new Image(),
            lockout     =   false,
            debug       =   options.debug || false,
            currURL     =   '';

        if(!camera_id) {
            // can't do anything without a camera_id
            return false;
        }

        // add preview image to calling div
        this.append(preview);
        $preview = $(preview);
        $buffer = $(buffer);

        $preview.width(width + 'px');
        $preview.height(height + 'px');

        function updatePreview() {
            currURL = '/image/' + camera_id + '?rand=' + Math.random()
            $buffer.attr('src', currURL);
            if(debug) console.log('jQuery.preview: updating image');
        }

        $buffer.on('load', function() {
            $preview.attr('src', currURL)
            setTimeout(updatePreview, delay)
        });


        $buffer.on('error', function() {
            if(debug) console.log('jQuery.preview: image error');
            setTimeout(updatePreview, delay)
        });


        //fetch the first image
        updatePreview();

        //return this to make it chainable
        return this;
    }

}(jQuery));
