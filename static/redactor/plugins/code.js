(function($)
{
    $.Redactor.prototype.codecolor = function()
    {
        return {
            init: function ()
            {

                var button = this.button.add('code', 'Code');
                this.button.addCallback(button, this.codecolor.execute);

            },
            execute: function (value)
            {
                console.log('code executed!')
            },
        };
    };
})(jQuery);