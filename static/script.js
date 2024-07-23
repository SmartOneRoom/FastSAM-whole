document.addEventListener('DOMContentLoaded', function() {
    const webcamFeed = document.getElementById('webcamFeed');
    const segmentation = document.getElementById('segmentation');

    // 웹캠 피드 URL 설정
    webcamFeed.src = '/video_feed';

    // 세그멘테이션 이미지 피드 URL 설정
    segmentation.src = '/segmentation_feed';
    segmentation.style.display = 'block';
});

