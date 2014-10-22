$(document).ready(function() {
    $('.carousel').carousel({
        interval: 5000 //changes the speed
    });
    var $validationModal, $emailRequired;

    $validationModal = modalDialog('#validation-sent-modal');
    $emailRequired = modalDialog('#email-required-modal');

    if (window.emailVerificationSent) {
        $validationModal.modal('show');
    }

    if (window.showEmailValidation) {
        $emailRequired.modal('show');
    }
});


var modalDialog = function (modalId, modalLinkName, submitHandler) {
    var $modal;
    $modal = $(modalId).modal({show: false});

    $modal.on('click', '.btn-primary', submitHandler || function (event) {
        event.preventDefault();
        if ($("#email").val().indexOf("@mail.utoronto.ca") > -1) {
            $("#email").parent().removeClass("has-error");
            $modal.find('form').submit();
        } else {
            $("#email").parent().addClass("has-error");
        }
    });

    if (modalLinkName) {
        $('a[name="' + modalLinkName + '"]').on('click', function (event) {
            event.preventDefault();
            $modal.modal('toggle');
        });
    }

    return $modal;
};
