const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// App.js가 루트에 있으므로, 바로 옆에 있는 public 폴더를 찾도록 수정했습니다.
app.use(express.static(path.join(__dirname, 'public')));

// 서버 상태 확인 API
app.get('/api/status', (req, res) => {
  // 서버가 어디에 있든 항상 한국(Asia/Seoul) 시간으로 계산합니다.
  const kstTime = new Date().toLocaleString('ko-KR', { timeZone: 'Asia/Seoul' });
  
  res.json({
    message: "GVIC 글로벌 서버가 가동 중입니다!",
    serverTime: kstTime,
    owner: "병각님"
  });
});
// 기본 페이지 설정
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, 'public/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});