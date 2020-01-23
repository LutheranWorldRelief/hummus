$(function () {
    $.fn.filer.defaults.captions = {
        button: gettext("Choose Files"),
        feedback: gettext("Choose files To Upload"),
        feedback2: gettext("files were chosen"),
        drop: gettext("Drop file here to Upload"),
        removeConfirmation: gettext("Are you sure you want to remove this file?"),
        errors: {
            filesLimit: gettext("Only {{fi-limit}} files are allowed to be uploaded."),
            filesType: gettext("Only Images are allowed to be uploaded."),
            filesSize: gettext("{{fi-name}} is too large! Please upload file up to {{fi-fileMaxSize}} MB."),
            filesSizeAll: gettext("Files you've choosed are too large! Please upload files up to {{fi-maxSize}} MB."),
            folderUpload: gettext("You are not allowed to upload folders."),
        }
    };
});