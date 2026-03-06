const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// App.js가 루트에 있으므로, 바로 옆에 있는 public 폴더를 찾도록 수정했습니다.
app.use(express.static(path.join(__dirname, 'public')));

// 서버 상태 확인 API
app.get('/api/status', (req, res) => {
  res.json({
    message: "서버가 아주 건강하게 작동 중입니다!",
    serverTime: new Date().toLocaleString('ko-KR'),
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