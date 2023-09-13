const camera = document.getElementById('camera');
const recordbutton = document.getElementById('record');
const sendbutton = document.getElementById('send');
let mediaRecorder;

const recorded = [];

async function startrecord(){
    const stream = await navigator.mediaDevices.getUserMedia(
        {
            video: true,
            audio: false
        }
    ).catch(err => console.error('カメラ取得エラー', err));
    
    camera.srcObject = stream;

    const options = {mimeType: 'video/webm;codecs=vp9,opus'}
    mediaRecorder = new MediaRecorder(stream, options);
    mediaRecorder.ondataavailable = (event) => {
        if (event.data && event.data.size > 0){
            recorded.push(event.data)
        }
    };

    mediaRecorder.start();
    console.log('録画開始');
    recordbutton.disabled = true;
    sendbutton.disabled = true;

    setTimeout(stoprecord, 10000);
}

function stoprecord(){
    mediaRecorder.stop();
    console.log('録画停止');
    mediaRecorder.onstop = () =>{
        recordbutton.disabled = false;
        sendbutton.disabled = false;
        camera.srcObject.getTracks().forEach(track => track.stop());
    };
}

recordbutton.addEventListener('click',() => {
    startrecord();
    recordbutton.disabled = true;
    sendbutton.disabled = true;
});
