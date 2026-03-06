const express = require('express');
const path = require('path');
const app = express();
const PORT = process.env.PORT || 3000;

// public 폴더 안의 파일들을 자동으로 웹에 보여줍니다.
app.use(express.static(path.join(__dirname, '../public')));

// 기본 주소로 접속했을 때 index.html을 보여줍니다.
app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, '../public/index.html'));
});

app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});