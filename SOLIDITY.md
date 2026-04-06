## План создания 20 NFT на Solidity

### Вот подробный план из 20 шагов для вашего знакомого: от генерации рисунков до запуска сайта для их продажи. План ориентирован на Solidity (ERC721), Polygon для низких комиссий и самостоятельный маркетплейс.

### Определите концепцию коллекции (тема, стиль рисунков, целевая аудитория для уникальности).

### Создайте 20 уникальных цифровых рисунков в Photoshop, GIMP или AI-инструментах вроде Midjourney.

### Измените размер изображений до 1000x1000 пикселей в формате PNG для стандарта NFT.

### Для каждого рисунка создайте JSON-метаданные: name, description, image (локальный путь), attributes (traits).

### Установите Node.js и создайте аккаунт на Pinata.cloud для IPFS-хранения.

### Загрузите 20 изображений на Pinata, получите IPFS-хэши (CID) для каждого (ipfs://Qm...).

### Обновите JSON-метаданные, заменив image на IPFS-ссылки изображений.

### Загрузите 20 JSON-файлов на Pinata, сохраните IPFS-URI для каждого NFT (ipfs://Qm.../1.json).

### Установите Remix IDE (remix.ethereum.org) для разработки Solidity.

### Создайте ERC721-контракт на Solidity: наследуйте от OpenZeppelin ERC721URIStorage, добавьте Counters для tokenId.

### В контракте добавьте функцию mint(address to, string uri), лимит maxSupply=20, onlyOwner.

### Скомпилируйте контракт в Remix, убедитесь в отсутствии ошибок.

### Создайте кошелек MetaMask, переключитесь на Polygon Mumbai testnet, получите тестовые MATIC из faucet.

### В Remix подключите MetaMask, задеплойте контракт на testnet (Injected Provider).

### Взаимодействуйте с контрактом: вызовите mint 20 раз для вашего адреса, передавая URI каждого NFT.

### Верифицируйте контракт на Polygonscan (скопируйте исходный код).

### Перейдите на Polygon mainnet, получите реальные MATIC (bridge с Ethereum), задеплойте mainnet-версию.

### Установите Node.js, создайте React-приложение (npx create-react-app nft-site), добавьте ethers.js, web3.js.

    Реализуйте frontend: подключение MetaMask, список NFT (fetch из контракта), mint/buy функции, дизайн с Tailwind.

    Деплойте сайт на Vercel/Netlify, протестируйте продажу/подарок (transferFrom), добавьте OpenSea-совместимость.
