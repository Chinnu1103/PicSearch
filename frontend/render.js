document.getElementById("choose_btn").addEventListener("click", function() {
    document.getElementById("file_name").value = "";
    file = null;
    document.getElementById('file_path').click();
});

function searchPhoto() {
    var apigClient = apigClientFactory.newClient();

    var user_message = document.getElementById('note-textarea').value;

    var body = {};
    var params = {q: user_message};
    var additionalParams = {
        headers: {
            'Content-Type': 'application/json',
        },
    };

    var images = document.getElementById('img-container').getElementsByTagName('img');
    for (var i = images.length - 1; i >= 0; i--) {
        images[i].parentNode.removeChild(images[i]);
    }

    document.getElementById('displaytext').textContent = 'Donloading Images..'
    document.getElementById('displaytext').style.display = 'block';

    apigClient
    .searchGet(params, body, additionalParams)
    .then(function (res) {
        var results = res.data.results;
        if (results.length == 0) {
            document.getElementById('displaytext').textContent = 'Sorry, I could not find any images for the given request';
            return;
        }


        results.forEach(function (obj) {
            document.getElementById('displaytext').style.display = 'none';        
            // Set the source of the image to the decoded Base64 string
            const img = new Image();
            img.src = obj.url;
            img.setAttribute('class', 'banner-img');
            img.setAttribute('alt', 'effy');
    
            // Append the image to an HTML element with ID 'img-container'
            document.getElementById('img-container').appendChild(img);
        });
    })
    .catch(function (result) {
    });
}

function uploadPhoto(file_obj) {
    $.ajax({
        url: 'https://wxh7uy0it9.execute-api.us-west-2.amazonaws.com/Version_0_0_2/upload/' + file_obj.name,
        type: 'PUT',
        data: file_obj,
        processData: false,
        contentType: false,
        headers: {
            'x-amz-meta-customLabels': note_customtag.value
        },
        success: function () {
            console.log('File uploaded successfully!');
        },
        error: function (xhr, status, error) {
            console.error('Error uploading file:', error);
        }
    });
}


const dropArea = document.querySelector(".drop_box"),
    button = dropArea.querySelector("button"),
    dragText = dropArea.querySelector("header"),
    input = dropArea.querySelector("input");
let file;
var filename;

button.onclick = () => {
    input.click();
};

document.getElementById("file_path").addEventListener("change", function (e) {
    var fileName = e.target.files[0].name;
    if(fileName){
        document.getElementById("file_name").value = fileName
        file = document.getElementById('file_path').files[0];
        console.log(file)
    }
});

