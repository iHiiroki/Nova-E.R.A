"""
interface.py — Interface visual completa da Nova E.R.A.

Contém o HTML da aplicação React (SPA) com:
  - Todos os 34 produtos e 8 categorias
  - Roteamento por hash (#/rota)
  - Carrinho persistido no localStorage
  - Autenticação com usuários demo
  - Animações de entrada, logo pulsante, filtros com fade
  - Todas as páginas: Home, Produtos, Produto, Carrinho,
    Login, Cadastro, Perfil, Sobre, Pedido Confirmado
"""

HTML = """<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Nova E.R.A. — Loja de Eletrônicos</title>
  <meta name="description" content="A melhor loja de eletrônicos do Brasil." />
  <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
  <link rel="preconnect" href="https://fonts.googleapis.com" />
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet" />
  <script src="https://unpkg.com/react@18/umd/react.development.js"></script>
  <script src="https://unpkg.com/react-dom@18/umd/react-dom.development.js"></script>
  <script src="https://unpkg.com/@babel/standalone/babel.min.js"></script>
  <style>
    /* ── Reset básico ── */
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }
    body { font-family: "Inter", sans-serif; background: #f8f7ff; color: #1a1a2e; }
    a    { color: inherit; }
    button, input, select, textarea { font-family: inherit; }
    img  { max-width: 100%; display: block; }

    /* ── Animações ── */
    @keyframes cardEntrada   { from { opacity:0; transform:translateY(28px) scale(.97) } to { opacity:1; transform:none } }
    @keyframes iconPulso     { 0%{transform:scale(1) rotate(0)} 30%{transform:scale(1.18) rotate(-10deg)} 60%{transform:scale(1.12) rotate(8deg)} 100%{transform:scale(1) rotate(0)} }
    @keyframes campoEntrada  { from { opacity:0; transform:translateX(-12px) } to { opacity:1; transform:none } }
    @keyframes erroEntrada   { from { opacity:0; transform:scale(.97) } to { opacity:1; transform:none } }
    @keyframes fadeSlideDown { from { opacity:0; transform:translateY(-6px) } to { opacity:1; transform:none } }
    @keyframes toastIn       { from { opacity:0; transform:translateY(20px) scale(.95) } to { opacity:1; transform:none } }
    @keyframes logoGlow      { 0%,100%{box-shadow:0 2px 8px rgba(124,58,237,.35)} 50%{box-shadow:0 4px 20px rgba(124,58,237,.65),0 0 0 4px rgba(124,58,237,.12)} }
    @keyframes gridFadeIn    { from { opacity:0; transform:translateY(10px) } to { opacity:1; transform:none } }

    /* ── Classes de animação ── */
    .logo-icon     { animation: logoGlow 3s ease-in-out infinite; transition: transform .2s; }
    .logo-icon:hover { transform: scale(1.08); }
    .produtos-grid { animation: gridFadeIn .28s cubic-bezier(.4,0,.2,1); }
    .menu-dropdown { animation: fadeSlideDown .18s ease; }

    /* ── Inputs com foco roxo ── */
    input:focus { border-color: #7c3aed !important; box-shadow: 0 0 0 3px rgba(124,58,237,.12); }
    input { transition: border-color .2s, box-shadow .2s; }
  </style>
</head>
<body>
<div id="root"></div>

<script type="text/babel" data-presets="react">
// =============================================================================
//  Nova E.R.A. — Loja de Eletrônicos
//  Aplicação React completa em arquivo único
// =============================================================================

const { useState, useEffect, useRef, createContext, useContext } = React;

// =============================================================================
// 1. DADOS — Produtos, Banners, Categorias, Usuários Demo
// =============================================================================

const PRODUTOS = [
  { id:1,  nome:"iPhone 15 Pro Max",          preco:8999.99,  preco_antigo:10499.99, categoria:"smartphones", marca:"Apple",      descricao:'Chip A17 Pro, câmera 48MP zoom 5x, tela Super Retina XDR 6.7".',                     imagemUrl:"https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:15, rating:4.9, novo:false },
  { id:2,  nome:"Samsung Galaxy S24 Ultra",   preco:7499.99,  preco_antigo:8999.99,  categoria:"smartphones", marca:"Samsung",    descricao:"S Pen integrada, câmera 200MP, zoom 10x, Snapdragon 8 Gen 3.",                       imagemUrl:"https://images.unsplash.com/photo-1610945415295-d9bbf067e59c?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:20, rating:4.8, novo:false },
  { id:3,  nome:"Google Pixel 9 Pro",         preco:5299.99,  preco_antigo:6499.99,  categoria:"smartphones", marca:"Google",     descricao:"Câmera computacional, 7 anos de atualizações Android, Magic Eraser.",                 imagemUrl:"https://images.unsplash.com/photo-1598327105666-5b89351aff97?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:18, rating:4.7, novo:true  },
  { id:4,  nome:"Motorola Edge 50 Ultra",     preco:3299.99,  preco_antigo:3999.99,  categoria:"smartphones", marca:"Motorola",   descricao:'Tela pOLED 6.7" 165Hz, câmera 50MP, carregamento 125W.',                             imagemUrl:"https://images.unsplash.com/photo-1567581935884-3349723552ca?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:25, rating:4.5, novo:true  },
  { id:5,  nome:"Xiaomi 14 Ultra",            preco:6499.99,  preco_antigo:7999.99,  categoria:"smartphones", marca:"Xiaomi",     descricao:'Câmera Leica 1" 50MP, Snapdragon 8 Gen 3, AMOLED 120Hz.',                            imagemUrl:"https://images.unsplash.com/photo-1574944985070-8f3ebc6b79d2?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:12, rating:4.6, novo:false },
  { id:6,  nome:'MacBook Pro 14" M3 Pro',     preco:12999.99, preco_antigo:14999.99, categoria:"notebooks",   marca:"Apple",      descricao:'Chip M3 Pro, tela Liquid Retina XDR 14", 18GB RAM, SSD 512GB.',                      imagemUrl:"https://images.unsplash.com/photo-1517336714731-489689fd1ca8?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:8,  rating:4.9, novo:false },
  { id:7,  nome:"Dell XPS 15 OLED",           preco:9499.99,  preco_antigo:10999.99, categoria:"notebooks",   marca:"Dell",       descricao:"Tela OLED 4K touch, Core Ultra 9, RTX 4070, 32GB RAM, SSD 1TB.",                     imagemUrl:"https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:5,  rating:4.7, novo:false },
  { id:8,  nome:"HP Spectre x360 14",         preco:8299.99,  preco_antigo:9999.99,  categoria:"notebooks",   marca:"HP",         descricao:"2-em-1 ultrafino, tela OLED WQXGA+, Core Ultra 7, caneta incluída.",                  imagemUrl:"https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:10, rating:4.6, novo:true  },
  { id:9,  nome:"Lenovo ThinkPad X1 Carbon",  preco:10499.99, preco_antigo:12499.99, categoria:"notebooks",   marca:"Lenovo",     descricao:"Ultrabook 1.12kg, tela IPS 2K, Core Ultra 7, bateria 15h.",                          imagemUrl:"https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:7,  rating:4.8, novo:false },
  { id:10, nome:"Asus ROG Zephyrus G16",      preco:11999.99, preco_antigo:13999.99, categoria:"notebooks",   marca:"Asus",       descricao:"Tela QHD 240Hz, RTX 4090, Ryzen 9 8945HS, 32GB DDR5.",                               imagemUrl:"https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:4,  rating:4.9, novo:true  },
  { id:11, nome:"Sony WH-1000XM5",            preco:1999.99,  preco_antigo:2499.99,  categoria:"audio",       marca:"Sony",       descricao:"Cancelamento ativo de ruído líder, 30h bateria, áudio Hi-Res.",                       imagemUrl:"https://images.unsplash.com/photo-1618366712010-f4ae9c647dcb?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:30, rating:4.8, novo:false },
  { id:12, nome:"Apple AirPods Pro 2",        preco:1649.99,  preco_antigo:1999.99,  categoria:"audio",       marca:"Apple",      descricao:"ANC personalizado, áudio espacial, rastreamento de cabeça, chip H2.",                 imagemUrl:"https://images.unsplash.com/photo-1588423771073-b8903fbb85b5?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:40, rating:4.9, novo:false },
  { id:13, nome:"Bose QuietComfort 45",       preco:1799.99,  preco_antigo:2199.99,  categoria:"audio",       marca:"Bose",       descricao:"ANC world-class, equalização Bose, 24h bateria, conforto superior.",                  imagemUrl:"https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:22, rating:4.7, novo:false },
  { id:14, nome:"JBL Charge 5 Wi-Fi",         preco:899.99,   preco_antigo:1099.99,  categoria:"audio",       marca:"JBL",        descricao:"Bluetooth + Wi-Fi, IP67, 20h bateria, USB-C.",                                       imagemUrl:"https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:45, rating:4.6, novo:false },
  { id:15, nome:"Sennheiser Momentum 4",      preco:2299.99,  preco_antigo:2799.99,  categoria:"audio",       marca:"Sennheiser", descricao:"60h autonomia, ANC adaptativo, qualidade Hi-Fi audiófilo.",                           imagemUrl:"https://images.unsplash.com/photo-1484704849700-f032a568e944?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:15, rating:4.8, novo:true  },
  { id:16, nome:'iPad Pro 13" M4',            preco:10999.99, preco_antigo:12999.99, categoria:"tablets",     marca:"Apple",      descricao:'Chip M4, tela OLED tandem 13", Apple Pencil Pro, Magic Keyboard.',                   imagemUrl:"https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:10, rating:4.9, novo:true  },
  { id:17, nome:"Samsung Galaxy Tab S9 Ultra",preco:6499.99,  preco_antigo:7999.99,  categoria:"tablets",     marca:"Samsung",    descricao:'AMOLED 14.6", S Pen incluída, Snapdragon 8 Gen 2, 12GB RAM.',                        imagemUrl:"https://images.unsplash.com/photo-1587095951604-b9d924a3fda0?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:14, rating:4.7, novo:false },
  { id:18, nome:"Xiaomi Pad 6 Pro",           preco:2499.99,  preco_antigo:3199.99,  categoria:"tablets",     marca:"Xiaomi",     descricao:"LCD 2.8K 144Hz, Snapdragon 8+ Gen 1, 8GB RAM, bateria 8600mAh.",                    imagemUrl:"https://images.unsplash.com/photo-1561154464-82e9adf32764?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:20, rating:4.5, novo:false },
  { id:19, nome:"Apple Watch Ultra 2",        preco:5999.99,  preco_antigo:7499.99,  categoria:"wearables",   marca:"Apple",      descricao:"GPS dupla frequência, tela 49mm, titânio, até 60h bateria.",                         imagemUrl:"https://images.unsplash.com/photo-1546868871-7041f2a55e12?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:10, rating:4.9, novo:false },
  { id:20, nome:"Samsung Galaxy Watch 7",     preco:1699.99,  preco_antigo:2199.99,  categoria:"wearables",   marca:"Samsung",    descricao:"Saúde avançada, GPS, AMOLED, até 40h bateria.",                                      imagemUrl:"https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:28, rating:4.6, novo:true  },
  { id:21, nome:"Garmin Fenix 7X Solar",      preco:4799.99,  preco_antigo:5999.99,  categoria:"wearables",   marca:"Garmin",     descricao:"Carregamento solar, 37 dias bateria, mapas topográficos.",                           imagemUrl:"https://images.unsplash.com/photo-1434494878577-86c23bcb06b9?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:8,  rating:4.8, novo:false },
  { id:22, nome:"Fitbit Charge 6",            preco:799.99,   preco_antigo:999.99,   categoria:"wearables",   marca:"Fitbit",     descricao:"GPS, cardíaco, SpO2, ECG, integração Google Maps.",                                  imagemUrl:"https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:35, rating:4.4, novo:false },
  { id:23, nome:'LG OLED C4 65"',             preco:7999.99,  preco_antigo:9999.99,  categoria:"tvs",         marca:"LG",         descricao:"OLED evo 4K, Dolby Vision IQ, 144Hz, HDMI 2.1.",                                     imagemUrl:"https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:6,  rating:4.9, novo:true  },
  { id:24, nome:'Samsung Neo QLED 8K 75"',    preco:9999.99,  preco_antigo:12999.99, categoria:"tvs",         marca:"Samsung",    descricao:"Neo QLED 8K, Quantum Matrix Pro, 240Hz, Tizen Smart TV.",                            imagemUrl:"https://images.unsplash.com/photo-1567690187548-f07b1d7bf5a9?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:3,  rating:4.7, novo:false },
  { id:25, nome:'Sony Bravia XR A95L 55"',    preco:8499.99,  preco_antigo:10499.99, categoria:"tvs",         marca:"Sony",       descricao:"QD-OLED, XR Cognitive, Triluminos Pro, Acoustic Surface Audio+.",                    imagemUrl:"https://images.unsplash.com/photo-1461151304267-38535e780c79?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:5,  rating:4.8, novo:false },
  { id:26, nome:"Sony Alpha A7 IV",           preco:15999.99, preco_antigo:18499.99, categoria:"cameras",     marca:"Sony",       descricao:"Mirrorless full-frame 33MP, IBIS 5 eixos, AF IA, 4K 60fps.",                        imagemUrl:"https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:6,  rating:4.9, novo:false },
  { id:27, nome:"Canon EOS R6 Mark II",       preco:12499.99, preco_antigo:14999.99, categoria:"cameras",     marca:"Canon",      descricao:"Full-frame 40MP, AF 40fps, estabilização 8 stops.",                                  imagemUrl:"https://images.unsplash.com/photo-1617005082133-548c4dd27f35?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:9,  rating:4.8, novo:true  },
  { id:28, nome:"GoPro Hero 13 Black",        preco:2199.99,  preco_antigo:2699.99,  categoria:"cameras",     marca:"GoPro",      descricao:"5.3K60, HyperSmooth 6.0, lentes intercambiáveis, à prova d'água.",                   imagemUrl:"https://images.unsplash.com/photo-1502920917128-1aa500764cbd?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:20, rating:4.7, novo:true  },
  { id:29, nome:"PlayStation 5 Slim",         preco:3999.99,  preco_antigo:4499.99,  categoria:"gaming",      marca:"Sony",       descricao:"4K, SSD ultra-rápido, ray tracing, som 3D, DualSense.",                              imagemUrl:"https://images.unsplash.com/photo-1607853202273-797f1c22a38e?w=500&h=500&fit=crop&auto=format", destaque:true,  estoque:15, rating:4.9, novo:false },
  { id:30, nome:"Xbox Series X",              preco:3799.99,  preco_antigo:4299.99,  categoria:"gaming",      marca:"Microsoft",  descricao:"4K 120fps, 1TB SSD NVMe, retrocompatibilidade 4 gerações.",                          imagemUrl:"https://images.unsplash.com/photo-1621259182978-fbf93132d53d?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:12, rating:4.8, novo:false },
  { id:31, nome:"Nintendo Switch OLED",       preco:2299.99,  preco_antigo:2699.99,  categoria:"gaming",      marca:"Nintendo",   descricao:'Híbrido portátil/TV, OLED 7", dock LAN, 64GB.',                                      imagemUrl:"https://images.unsplash.com/photo-1578303512597-81e6cc155b3e?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:22, rating:4.8, novo:false },
  { id:32, nome:"Amazon Echo Hub",            preco:1099.99,  preco_antigo:1399.99,  categoria:"smarthome",   marca:"Amazon",     descricao:'Smart display 8" Alexa, hub Matter, Zigbee, Z-Wave.',                                imagemUrl:"https://images.unsplash.com/photo-1512446816042-444d641267d4?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:25, rating:4.5, novo:true  },
  { id:33, nome:"Google Nest Hub Max",        preco:1299.99,  preco_antigo:1599.99,  categoria:"smarthome",   marca:"Google",     descricao:'Smart display 10" câmera, reconhecimento facial, controle smart home.',               imagemUrl:"https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:18, rating:4.6, novo:false },
  { id:34, nome:"Philips Hue Starter Kit",    preco:699.99,   preco_antigo:899.99,   categoria:"smarthome",   marca:"Philips",    descricao:"3 lâmpadas E27 coloridas, hub Bridge, 16M cores, compatível Alexa.",                 imagemUrl:"https://images.unsplash.com/photo-1621600411688-4be93cd68504?w=500&h=500&fit=crop&auto=format", destaque:false, estoque:30, rating:4.6, novo:false },
];

const BANNERS = [
  { tag:"Novidades 2026", cor:"#7c3aed", titulo:"iPhone 15 Pro Max",  subtitulo:"Chip A17 Pro. Câmera Profissional. Design Titânio.",   img:"https://images.unsplash.com/photo-1695048133142-1a20484d2569?w=1400&h=500&fit=crop&auto=format", btn:"Ver Produto",   link:"/produto/1"  },
  { tag:"Até 30% OFF",    cor:"#f59e0b", titulo:"Asus ROG Zephyrus",  subtitulo:"RTX 4090. QHD 240Hz. O notebook gamer definitivo.",    img:"https://images.unsplash.com/photo-1603302576837-37561b2e2302?w=1400&h=500&fit=crop&auto=format", btn:"Conferir",      link:"/produto/10" },
  { tag:"Lançamento",     cor:"#f43f5e", titulo:"Sony Alpha A7 IV",   subtitulo:"Full-Frame 33MP. Autofoco por IA. 4K 60fps.",          img:"https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=1400&h=500&fit=crop&auto=format", btn:"Saiba Mais",    link:"/produto/26" },
  { tag:"Super Oferta",   cor:"#0d9488", titulo:"PlayStation 5 Slim", subtitulo:"4K. Ray Tracing. SSD Ultra-Rápido. DualSense.",        img:"https://images.unsplash.com/photo-1607853202273-797f1c22a38e?w=1400&h=500&fit=crop&auto=format", btn:"Comprar Agora", link:"/produto/29" },
];

const CATEGORIAS = [
  { slug:"smartphones", icon:"📱", label:"Smartphones" },
  { slug:"notebooks",   icon:"💻", label:"Notebooks"   },
  { slug:"audio",       icon:"🎧", label:"Áudio"        },
  { slug:"tablets",     icon:"📟", label:"Tablets"      },
  { slug:"wearables",   icon:"⌚", label:"Wearables"    },
  { slug:"tvs",         icon:"📺", label:"TVs"          },
  { slug:"cameras",     icon:"📷", label:"Câmeras"      },
  { slug:"gaming",      icon:"🎮", label:"Gaming"       },
];

const CAT_ICONS = {
  smartphones:"📱", notebooks:"💻", audio:"🎧", tablets:"📟",
  wearables:"⌚", tvs:"📺", cameras:"📷", gaming:"🎮", smarthome:"🏠",
};

const DEMO_USERS = {
  "joao@email.com":  { senha:"123456", nome:"João Silva",   telefone:"(11) 98765-4321", cpf:"123.456.789-00", endereco:"Rua das Flores, 42 — São Paulo/SP" },
  "maria@email.com": { senha:"123456", nome:"Maria Santos", telefone:"(21) 91234-5678", cpf:"987.654.321-00", endereco:"Av. Copacabana, 100 — Rio de Janeiro/RJ" },
};

// =============================================================================
// 2. FUNÇÕES UTILITÁRIAS
// =============================================================================

function fmtPreco(valor) {
  return "R$ " + valor.toFixed(2).replace(".", ",").replace(/\\B(?=(\\d{3})+(?!\\d))/g, ".");
}

function descontoPct(preco, precoAntigo) {
  return Math.round((1 - preco / precoAntigo) * 100);
}

function estrelas(rating) {
  const cheias = Math.round(rating);
  return "★".repeat(cheias) + "☆".repeat(5 - cheias);
}

// =============================================================================
// 3. ROTEADOR — navegação por hash (#/rota)
// =============================================================================

function useHash() {
  const [hash, setHash] = useState(window.location.hash || "#/");
  useEffect(() => {
    const fn = () => setHash(window.location.hash || "#/");
    window.addEventListener("hashchange", fn);
    return () => window.removeEventListener("hashchange", fn);
  }, []);
  return hash;
}

function navegar(caminho) {
  window.location.hash = "#" + caminho;
  window.scrollTo({ top: 0, behavior: "smooth" });
}

// Faz o parse do hash para extrair rota e parâmetros de query
function parsearHash(hash) {
  const semHash    = hash.replace(/^#/, "") || "/";
  const partePath  = semHash.split("?")[0];
  const parteQuery = semHash.includes("?") ? semHash.split("?")[1] : "";
  const params     = new URLSearchParams(parteQuery);
  const partes     = partePath.split("/").filter(Boolean);
  return { partes, params };
}

// =============================================================================
// 4. CONTEXTOS — Carrinho, Autenticação, Toast
// =============================================================================

// ── Carrinho ──────────────────────────────────────────────────────────────────
const CartContext = createContext();

function CartProvider({ children }) {
  const [items, setItems] = useState(() => {
    try { return JSON.parse(localStorage.getItem("nova_era_cart") || "[]"); }
    catch { return []; }
  });

  useEffect(() => {
    localStorage.setItem("nova_era_cart", JSON.stringify(items));
  }, [items]);

  function addItem(produto, quantidade = 1) {
    setItems(prev => {
      const existente = prev.find(i => i.produto_id === produto.id);
      if (existente)
        return prev.map(i => i.produto_id === produto.id
          ? { ...i, quantidade: i.quantidade + quantidade } : i);
      return [...prev, {
        produto_id: produto.id, nome: produto.nome, marca: produto.marca,
        preco: produto.preco, imagemUrl: produto.imagemUrl, quantidade,
      }];
    });
  }

  function removeItem(id) { setItems(prev => prev.filter(i => i.produto_id !== id)); }

  function updateQty(id, novaQty) {
    if (novaQty < 1) { removeItem(id); return; }
    setItems(prev => prev.map(i => i.produto_id === id ? { ...i, quantidade: novaQty } : i));
  }

  function clearCart() { setItems([]); }

  const totalItems = items.reduce((s, i) => s + i.quantidade, 0);
  const totalValor = items.reduce((s, i) => s + i.preco * i.quantidade, 0);

  return (
    <CartContext.Provider value={{ items, addItem, removeItem, updateQty, clearCart, totalItems, totalValor }}>
      {children}
    </CartContext.Provider>
  );
}

function useCart() { return useContext(CartContext); }

// ── Autenticação ──────────────────────────────────────────────────────────────
const AuthContext = createContext();

function AuthProvider({ children }) {
  const [usuario, setUsuario] = useState(() => {
    try { return JSON.parse(localStorage.getItem("nova_era_usuario") || "null"); }
    catch { return null; }
  });

  function login(dados) {
    localStorage.setItem("nova_era_usuario", JSON.stringify(dados));
    setUsuario(dados);
  }

  function logout() {
    localStorage.removeItem("nova_era_usuario");
    setUsuario(null);
  }

  function updateUser(dados) {
    const atualizado = { ...usuario, ...dados };
    localStorage.setItem("nova_era_usuario", JSON.stringify(atualizado));
    setUsuario(atualizado);
  }

  return (
    <AuthContext.Provider value={{ usuario, login, logout, updateUser }}>
      {children}
    </AuthContext.Provider>
  );
}

function useAuth() { return useContext(AuthContext); }

// ── Toast — notificações no rodapé da tela ────────────────────────────────────
const ToastContext = createContext();

function ToastProvider({ children }) {
  const [msg, setMsg] = useState(null);
  const timerRef = useRef(null);

  function showToast(mensagem) {
    if (timerRef.current) clearTimeout(timerRef.current);
    setMsg(mensagem);
    timerRef.current = setTimeout(() => setMsg(null), 3000);
  }

  return (
    <ToastContext.Provider value={{ showToast }}>
      {children}
      {msg && (
        <div style={{
          position:"fixed", bottom:"2rem", left:"50%", transform:"translateX(-50%)",
          background:"#1a1a2e", color:"#fff", padding:"0.85rem 1.75rem",
          borderRadius:12, fontSize:"0.92rem", fontWeight:600, zIndex:9999,
          boxShadow:"0 8px 32px rgba(0,0,0,.25)", animation:"toastIn .3s ease",
          whiteSpace:"nowrap",
        }}>
          {msg}
        </div>
      )}
    </ToastContext.Provider>
  );
}

function useToast() { return useContext(ToastContext); }

// =============================================================================
// 5. COMPONENTES REUTILIZÁVEIS — ProdutoCard, Navbar, Footer
// =============================================================================

// ── Card de produto ───────────────────────────────────────────────────────────
function ProdutoCard({ produto }) {
  const { addItem }    = useCart();
  const { showToast }  = useToast();
  const [adicionado, setAdicionado] = useState(false);
  const [imgErro, setImgErro]       = useState(false);

  const descPct = produto.preco_antigo ? descontoPct(produto.preco, produto.preco_antigo) : 0;
  const icon    = CAT_ICONS[produto.categoria] || "📦";

  function adicionar(e) {
    e.preventDefault();
    addItem(produto);
    setAdicionado(true);
    showToast("✓ " + produto.nome + " adicionado ao carrinho!");
    setTimeout(() => setAdicionado(false), 1800);
  }

  return (
    <div
      style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, overflow:"hidden", transition:"box-shadow .3s, transform .3s", display:"flex", flexDirection:"column" }}
      onMouseEnter={e => { e.currentTarget.style.boxShadow = "0 4px 16px rgba(124,58,237,.12)"; e.currentTarget.style.transform = "translateY(-5px)"; }}
      onMouseLeave={e => { e.currentTarget.style.boxShadow = "none"; e.currentTarget.style.transform = "none"; }}
    >
      {/* Imagem */}
      <a href={"#/produto/" + produto.id} style={{ display:"block", position:"relative", textDecoration:"none" }}>
        <div style={{ width:"100%", paddingBottom:"100%", position:"relative", background:"#f8f7ff", overflow:"hidden" }}>
          {!imgErro ? (
            <img
              src={produto.imagemUrl} alt={produto.nome} loading="lazy"
              onError={() => setImgErro(true)}
              style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover", objectPosition:"center", transition:"transform .45s" }}
            />
          ) : (
            <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", background:"linear-gradient(135deg,#ede9fe,#f5f3ff)", fontSize:"3rem" }}>
              {icon}
            </div>
          )}
          {descPct > 0  && <span style={{ position:"absolute", top:"0.65rem", left:"0.65rem",  background:"#f43f5e", color:"#fff", fontSize:"0.72rem", fontWeight:700, padding:"0.2rem 0.5rem", borderRadius:6 }}>-{descPct}%</span>}
          {produto.novo && <span style={{ position:"absolute", top:"0.65rem", right:"0.65rem", background:"#0d9488", color:"#fff", fontSize:"0.68rem", fontWeight:700, padding:"0.2rem 0.5rem", borderRadius:6 }}>Novo</span>}
        </div>
      </a>

      {/* Informações */}
      <div style={{ padding:"0.9rem", display:"flex", flexDirection:"column", flex:1 }}>
        <span style={{ fontSize:"0.72rem", fontWeight:700, color:"#7c3aed", textTransform:"uppercase", letterSpacing:"0.06em", display:"block", marginBottom:"0.25rem" }}>
          {produto.marca}
        </span>
        <a href={"#/produto/" + produto.id} style={{ fontWeight:700, fontSize:"0.9rem", color:"#1a1a2e", display:"block", marginBottom:"0.3rem", lineHeight:1.35, textDecoration:"none", flex:1 }}>
          {produto.nome}
        </a>
        <div style={{ fontSize:"0.78rem", color:"#f59e0b", marginBottom:"0.5rem" }}>
          {estrelas(produto.rating)} <span style={{ color:"#64748b" }}>{produto.rating}</span>
        </div>
        <div style={{ display:"flex", alignItems:"center", gap:"0.5rem", flexWrap:"wrap", marginBottom:"0.65rem" }}>
          {produto.preco_antigo && <span style={{ fontSize:"0.78rem", color:"#64748b", textDecoration:"line-through" }}>{fmtPreco(produto.preco_antigo)}</span>}
          <span style={{ fontSize:"1rem", fontWeight:800, color:"#1a1a2e" }}>{fmtPreco(produto.preco)}</span>
        </div>
        <button onClick={adicionar} style={{
          display:"flex", alignItems:"center", justifyContent:"center", gap:"0.4rem",
          padding:"0.42rem 0.85rem", borderRadius:10, width:"100%",
          background: adicionado ? "#16a34a" : "linear-gradient(135deg,#7c3aed,#8b5cf6)",
          color:"#fff", fontWeight:600, fontSize:"0.82rem", border:"none", cursor:"pointer", transition:"all .2s",
        }}>
          {adicionado ? "✓ Adicionado" : "🛒 Adicionar"}
        </button>
      </div>
    </div>
  );
}

// ── Navbar ────────────────────────────────────────────────────────────────────
function Navbar() {
  const { totalItems }     = useCart();
  const { usuario, logout } = useAuth();
  const [menuAberto, setMenuAberto] = useState(false);
  const menuRef = useRef(null);
  const hash    = useHash();

  useEffect(() => {
    const fn = (e) => { if (menuRef.current && !menuRef.current.contains(e.target)) setMenuAberto(false); };
    document.addEventListener("mousedown", fn);
    return () => document.removeEventListener("mousedown", fn);
  }, []);

  useEffect(() => { setMenuAberto(false); }, [hash]);

  return (
    <nav style={{ background:"#fff", borderBottom:"1px solid #e5e4f5", position:"sticky", top:0, zIndex:200, boxShadow:"0 1px 3px rgba(124,58,237,.06),0 4px 12px rgba(124,58,237,.04)" }}>
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem", display:"flex", alignItems:"center", gap:"2rem", height:66 }}>

        {/* Logo animado */}
        <a href="#/" style={{ fontWeight:800, fontSize:"1.4rem", display:"flex", gap:"0.5rem", alignItems:"center", textDecoration:"none" }}>
          <div className="logo-icon" style={{ width:36, height:36, borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", display:"flex", alignItems:"center", justifyContent:"center", flexShrink:0 }}>
            <span style={{ fontSize:"1rem" }}>⚡</span>
          </div>
          <span>
            <span style={{ color:"#1a1a2e" }}>Nova</span>
            <span style={{ color:"#7c3aed" }}>E.R.A.</span>
          </span>
        </a>

        {/* Links */}
        <div style={{ display:"flex", gap:"1.5rem", flex:1 }}>
          <a href="#/produtos" style={{ color:"#64748b", fontWeight:500, fontSize:"0.95rem", textDecoration:"none" }}>Produtos</a>
          <a href="#/sobre"    style={{ color:"#64748b", fontWeight:500, fontSize:"0.95rem", textDecoration:"none" }}>Sobre</a>
        </div>

        {/* Ações */}
        <div style={{ display:"flex", alignItems:"center", gap:"0.6rem" }}>
          <a href="#/produtos" style={{ display:"flex", alignItems:"center", justifyContent:"center", width:40, height:40, borderRadius:10, color:"#64748b", textDecoration:"none", fontSize:"1.1rem" }}>🔍</a>

          <a href="#/carrinho" style={{ display:"flex", alignItems:"center", justifyContent:"center", width:40, height:40, borderRadius:10, color:"#64748b", textDecoration:"none", fontSize:"1.15rem", position:"relative" }}>
            🛍️
            {totalItems > 0 && (
              <span style={{ position:"absolute", top:-5, right:-5, background:"#f43f5e", color:"#fff", fontSize:"0.62rem", fontWeight:700, minWidth:18, height:18, borderRadius:9, display:"flex", alignItems:"center", justifyContent:"center", padding:"0 4px" }}>
                {totalItems}
              </span>
            )}
          </a>

          {usuario ? (
            <div ref={menuRef} style={{ position:"relative" }}>
              <button onClick={() => setMenuAberto(v => !v)} title={usuario.nome}
                style={{ width:38, height:38, borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", border:"none", cursor:"pointer", display:"flex", alignItems:"center", justifyContent:"center", fontSize:"1rem" }}>
                👤
              </button>
              {menuAberto && (
                <div className="menu-dropdown" style={{ position:"absolute", top:"calc(100% + 10px)", right:0, background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, boxShadow:"0 8px 32px rgba(124,58,237,.18)", minWidth:210, overflow:"hidden", zIndex:300 }}>
                  <div style={{ padding:"1rem", borderBottom:"1px solid #e5e4f5", background:"linear-gradient(135deg,#ede9fe,#f5f3ff)" }}>
                    <p style={{ fontWeight:700, fontSize:"0.92rem", color:"#6d28d9" }}>{usuario.nome}</p>
                    <p style={{ color:"#64748b", fontSize:"0.78rem", marginTop:"0.1rem" }}>{usuario.email}</p>
                  </div>
                  <a href="#/perfil"              style={{ display:"flex", alignItems:"center", gap:"0.6rem", padding:"0.75rem 1rem", fontSize:"0.88rem", color:"#1a1a2e", textDecoration:"none" }}>👤 Meu Perfil</a>
                  <a href="#/perfil?tab=pedidos"  style={{ display:"flex", alignItems:"center", gap:"0.6rem", padding:"0.75rem 1rem", fontSize:"0.88rem", color:"#1a1a2e", textDecoration:"none" }}>📦 Meus Pedidos</a>
                  <button onClick={logout}        style={{ width:"100%", display:"flex", alignItems:"center", gap:"0.6rem", padding:"0.75rem 1rem", fontSize:"0.88rem", color:"#dc2626", background:"none", border:"none", cursor:"pointer", textAlign:"left" }}>↩ Sair</button>
                </div>
              )}
            </div>
          ) : (
            <>
              <a href="#/login"    style={{ display:"inline-flex", alignItems:"center", gap:"0.5rem", padding:"0.55rem 1.1rem", borderRadius:10, fontWeight:600, fontSize:"0.88rem", border:"2px solid #7c3aed", color:"#7c3aed", textDecoration:"none" }}>→ Entrar</a>
              <a href="#/cadastro" style={{ display:"inline-flex", alignItems:"center", gap:"0.5rem", padding:"0.55rem 1.1rem", borderRadius:10, fontWeight:600, fontSize:"0.88rem", background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", textDecoration:"none" }}>✚ Cadastrar</a>
            </>
          )}
        </div>
      </div>
    </nav>
  );
}

// ── Rodapé ────────────────────────────────────────────────────────────────────
function Footer() {
  return (
    <footer style={{ background:"#1a1a2e", color:"#a78bfa", padding:"2.5rem 0", marginTop:"3rem" }}>
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem", display:"flex", justifyContent:"space-between", alignItems:"center", flexWrap:"wrap", gap:"1rem" }}>
        <div style={{ display:"flex", alignItems:"center", gap:"0.6rem" }}>
          <div style={{ width:32, height:32, borderRadius:9, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", display:"flex", alignItems:"center", justifyContent:"center" }}>⚡</div>
          <span style={{ fontWeight:800, color:"#fff", fontSize:"1.1rem" }}>Nova<span style={{ color:"#a78bfa" }}>E.R.A.</span></span>
        </div>
        <p style={{ fontSize:"0.85rem", color:"#64748b" }}>© 2026 Nova E.R.A. Todos os direitos reservados.</p>
        <div style={{ display:"flex", gap:"1.25rem" }}>
          {[["#/produtos","Produtos"],["#/sobre","Sobre"],["#/carrinho","Carrinho"]].map(([href,label]) => (
            <a key={href} href={href} style={{ color:"#64748b", fontSize:"0.85rem", textDecoration:"none" }}>{label}</a>
          ))}
        </div>
      </div>
    </footer>
  );
}

// =============================================================================
// 6. PÁGINAS
// =============================================================================

// ── Home ──────────────────────────────────────────────────────────────────────
function Home() {
  const [slide, setSlide] = useState(0);
  const [sort, setSort]   = useState("relevancia");
  const autoRef = useRef(null);

  function irPara(idx) { setSlide((idx + BANNERS.length) % BANNERS.length); }
  function proximo()   { irPara(slide + 1); }
  function anterior()  { irPara(slide - 1); }
  function iniciarAuto() { autoRef.current = setInterval(proximo, 5200); }
  function pararAuto()   { if (autoRef.current) clearInterval(autoRef.current); }

  useEffect(() => { iniciarAuto(); return pararAuto; }, [slide]);

  let todos = [...PRODUTOS];
  if (sort === "preco-asc")  todos.sort((a, b) => a.preco - b.preco);
  if (sort === "preco-desc") todos.sort((a, b) => b.preco - a.preco);
  if (sort === "az")         todos.sort((a, b) => a.nome.localeCompare(b.nome));
  if (sort === "za")         todos.sort((a, b) => b.nome.localeCompare(a.nome));

  const destaques  = PRODUTOS.filter(p => p.destaque).slice(0, 8);
  const beneficios = [
    { icon:"🚚", titulo:"Frete Grátis",       desc:"Acima de R$ 500 para todo o Brasil" },
    { icon:"🛡️", titulo:"Garantia Estendida", desc:"12 meses em todos os produtos"       },
    { icon:"💳", titulo:"12x Sem Juros",       desc:"Parcelamento no cartão de crédito"   },
    { icon:"↩️", titulo:"Troca em 30 dias",   desc:"Sem burocracia, sem complicação"     },
  ];

  return (
    <div>
      {/* Banner carrossel */}
      <section style={{ overflow:"hidden", position:"relative", background:"#1a1a2e" }}>
        <div style={{ overflow:"hidden" }}>
          <div style={{ display:"flex", transform:"translateX(-" + (slide * 100) + "%)", transition:"transform .55s cubic-bezier(.4,0,.2,1)" }}>
            {BANNERS.map((b, i) => (
              <div key={i} style={{ minWidth:"100%", position:"relative", height:420, overflow:"hidden", flexShrink:0 }}>
                <img src={b.img} alt={b.titulo} style={{ width:"100%", height:"100%", objectFit:"cover", objectPosition:"center", opacity:.45 }} />
                <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center" }}>
                  <div style={{ padding:"0 4rem", maxWidth:600 }}>
                    <span style={{ display:"inline-block", background:b.cor, color:"#fff", padding:"0.25rem 0.85rem", borderRadius:100, fontSize:"0.78rem", fontWeight:700, letterSpacing:"0.06em", marginBottom:"0.75rem" }}>{b.tag}</span>
                    <h2 style={{ fontSize:"2.6rem", fontWeight:900, color:"#fff", lineHeight:1.15, marginBottom:"0.75rem" }}>{b.titulo}</h2>
                    <p style={{ color:"#cbd5e1", fontSize:"1rem", marginBottom:"1.5rem" }}>{b.subtitulo}</p>
                    <a href={"#" + b.link} style={{ display:"inline-flex", alignItems:"center", gap:"0.5rem", padding:"0.85rem 1.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"1rem", textDecoration:"none" }}>{b.btn}</a>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
        <div style={{ position:"absolute", bottom:"1.25rem", left:"50%", transform:"translateX(-50%)", display:"flex", gap:"0.5rem", zIndex:10 }}>
          {BANNERS.map((_, i) => <button key={i} onClick={() => { pararAuto(); irPara(i); }} style={{ width:i===slide?28:8, height:8, borderRadius:4, background:i===slide?"#fff":"rgba(255,255,255,.4)", border:"none", cursor:"pointer", transition:"all .35s" }} />)}
        </div>
        <div style={{ position:"absolute", top:"50%", transform:"translateY(-50%)", width:"100%", display:"flex", justifyContent:"space-between", padding:"0 1rem", pointerEvents:"none", zIndex:10 }}>
          {[anterior, proximo].map((fn, i) => (
            <button key={i} onClick={() => { pararAuto(); fn(); }} style={{ width:44, height:44, borderRadius:"50%", background:"rgba(255,255,255,.15)", border:"1.5px solid rgba(255,255,255,.3)", color:"#fff", display:"flex", alignItems:"center", justifyContent:"center", cursor:"pointer", pointerEvents:"all", fontSize:"1.25rem" }}>
              {i === 0 ? "‹" : "›"}
            </button>
          ))}
        </div>
      </section>

      {/* Categorias */}
      <section style={{ padding:"3.5rem 0" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
          <h2 style={{ fontSize:"1.8rem", fontWeight:800, marginBottom:"1.5rem" }}>Explore por Categoria</h2>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(8,1fr)", gap:"0.85rem" }}>
            {CATEGORIAS.map(cat => (
              <a key={cat.slug} href={"#/produtos?categoria=" + cat.slug} style={{ textDecoration:"none" }}>
                <div
                  style={{ display:"flex", flexDirection:"column", alignItems:"center", gap:"0.5rem", padding:"1.25rem 0.75rem", background:"#fff", border:"2px solid #e5e4f5", borderRadius:14, textAlign:"center", cursor:"pointer", transition:"all .25s" }}
                  onMouseEnter={e => Object.assign(e.currentTarget.style, { borderColor:"#7c3aed", transform:"translateY(-5px)", background:"#ede9fe", boxShadow:"0 4px 16px rgba(124,58,237,.12)" })}
                  onMouseLeave={e => Object.assign(e.currentTarget.style, { borderColor:"#e5e4f5", transform:"", background:"#fff", boxShadow:"" })}
                >
                  <span style={{ fontSize:"1.75rem" }}>{cat.icon}</span>
                  <p style={{ fontSize:"0.78rem", fontWeight:700, color:"#64748b", margin:0 }}>{cat.label}</p>
                </div>
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* Produtos em destaque */}
      <section style={{ padding:"0 0 2rem" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
          <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:"1.5rem" }}>
            <h2 style={{ fontSize:"1.8rem", fontWeight:800 }}>🔥 Produtos em Destaque</h2>
            <a href="#/produtos" style={{ color:"#7c3aed", fontWeight:600, fontSize:"0.9rem", textDecoration:"none" }}>Ver todos →</a>
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))", gap:"1.25rem" }}>
            {destaques.map(p => <ProdutoCard key={p.id} produto={p} />)}
          </div>
        </div>
      </section>

      {/* Todos os produtos */}
      <section style={{ padding:"2rem 0 4rem" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
          <h2 style={{ fontSize:"1.8rem", fontWeight:800, marginBottom:"1rem" }}>🛍️ Todos os Produtos</h2>
          <div style={{ display:"flex", alignItems:"center", gap:"0.5rem", flexWrap:"wrap", marginBottom:"1.25rem" }}>
            <span style={{ fontSize:"0.85rem", color:"#64748b", fontWeight:600 }}>Ordenar por:</span>
            {[["relevancia","Relevância"],["preco-asc","Menor Preço"],["preco-desc","Maior Preço"],["az","A→Z"],["za","Z→A"]].map(([k,l]) => (
              <button key={k} onClick={() => setSort(k)} style={{ padding:"0.4rem 0.9rem", borderRadius:100, border:"1.5px solid "+(sort===k?"#7c3aed":"#e5e4f5"), background:sort===k?"#ede9fe":"#fff", color:sort===k?"#7c3aed":"#64748b", fontSize:"0.82rem", fontWeight:600, cursor:"pointer", transition:"all .2s" }}>{l}</button>
            ))}
          </div>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))", gap:"1.25rem" }}>
            {todos.map(p => <ProdutoCard key={p.id} produto={p} />)}
          </div>
        </div>
      </section>

      {/* Benefícios */}
      <section style={{ padding:"3.5rem 0", background:"#fff" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
          <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:"1.25rem" }}>
            {beneficios.map((b, i) => (
              <div key={i}
                style={{ textAlign:"center", padding:"2rem 1.5rem", background:"#f8f7ff", border:"1px solid #e5e4f5", borderRadius:14, transition:"all .25s" }}
                onMouseEnter={e => Object.assign(e.currentTarget.style, { borderColor:"#7c3aed", boxShadow:"0 4px 16px rgba(124,58,237,.12)", transform:"translateY(-4px)" })}
                onMouseLeave={e => Object.assign(e.currentTarget.style, { borderColor:"#e5e4f5", boxShadow:"", transform:"" })}
              >
                <div style={{ fontSize:"2rem", marginBottom:"0.75rem" }}>{b.icon}</div>
                <h3 style={{ fontSize:"0.95rem", fontWeight:700, marginBottom:"0.35rem" }}>{b.titulo}</h3>
                <p style={{ fontSize:"0.82rem", color:"#64748b" }}>{b.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>
    </div>
  );
}

// ── Lista de Produtos ─────────────────────────────────────────────────────────
function Produtos({ params }) {
  const [categoria,   setCategoria]   = useState(params.get("categoria") || "");
  const [busca,       setBusca]       = useState(params.get("busca") || "");
  const [inputBusca,  setInputBusca]  = useState(busca);
  const [sort,        setSort]        = useState("");
  const [animKey,     setAnimKey]     = useState(0);

  function triggerAnim()       { setAnimKey(k => k + 1); }
  function filtrarCategoria(s) { setCategoria(s); triggerAnim(); }
  function filtrarSort(k)      { setSort(k); triggerAnim(); }
  function buscar(e)           { e.preventDefault(); setBusca(inputBusca); triggerAnim(); }
  function limpar()            { setBusca(""); setInputBusca(""); setCategoria(""); triggerAnim(); }

  let lista = [...PRODUTOS];
  if (categoria) lista = lista.filter(p => p.categoria === categoria);
  if (busca) {
    const bl = busca.toLowerCase();
    lista = lista.filter(p => p.nome.toLowerCase().includes(bl) || p.marca.toLowerCase().includes(bl) || p.descricao.toLowerCase().includes(bl));
  }
  if (sort === "preco-asc")  lista.sort((a, b) => a.preco - b.preco);
  if (sort === "preco-desc") lista.sort((a, b) => b.preco - a.preco);
  if (sort === "az")         lista.sort((a, b) => a.nome.localeCompare(b.nome));
  if (sort === "za")         lista.sort((a, b) => b.nome.localeCompare(a.nome));

  const btnCatStyle = (ativo) => ({
    display:"flex", alignItems:"center", gap:"0.5rem", padding:"0.5rem 0.75rem",
    borderRadius:8, fontSize:"0.86rem", border:"none", textAlign:"left",
    background: ativo ? "#ede9fe" : "transparent",
    color:      ativo ? "#7c3aed" : "#64748b",
    fontWeight: ativo ? 700       : 400,
    cursor:"pointer", transition:"all .18s",
  });

  return (
    <div>
      <style>{".produtos-grid { animation: gridFadeIn .28s cubic-bezier(.4,0,.2,1); }"}</style>

      <div style={{ background:"linear-gradient(135deg,#1a1a2e,#2e1065)", color:"#fff", padding:"2.75rem 0", marginBottom:"2rem" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
          <h1 style={{ fontSize:"2rem", fontWeight:800 }}>Nossos Produtos</h1>
          <p style={{ color:"#a78bfa", marginTop:"0.4rem", fontSize:"0.95rem" }}>Encontre o eletrônico perfeito para você</p>
        </div>
      </div>

      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem 4rem" }}>
        <div style={{ display:"grid", gridTemplateColumns:"230px 1fr", gap:"2rem" }}>

          {/* Sidebar */}
          <aside>
            <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"1.25rem", marginBottom:"1rem" }}>
              <h3 style={{ fontSize:"0.82rem", fontWeight:700, marginBottom:"0.75rem", color:"#64748b", textTransform:"uppercase", letterSpacing:"0.07em" }}>Buscar</h3>
              <form onSubmit={buscar} style={{ display:"flex", flexDirection:"column", gap:"0.5rem" }}>
                <input type="text" value={inputBusca} onChange={e => setInputBusca(e.target.value)} placeholder="Nome ou marca..."
                  style={{ padding:"0.65rem 0.95rem", border:"1.5px solid #e5e4f5", borderRadius:10, fontSize:"0.9rem", outline:"none" }} />
                <button type="submit" style={{ padding:"0.6rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"0.9rem", border:"none", cursor:"pointer" }}>Buscar</button>
                {(busca || categoria) && (
                  <button type="button" onClick={limpar} style={{ padding:"0.6rem", borderRadius:10, background:"transparent", color:"#7c3aed", fontWeight:600, fontSize:"0.9rem", border:"2px solid #7c3aed", cursor:"pointer" }}>Limpar filtros</button>
                )}
              </form>
            </div>
            <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"1.25rem" }}>
              <h3 style={{ fontSize:"0.82rem", fontWeight:700, marginBottom:"0.75rem", color:"#64748b", textTransform:"uppercase", letterSpacing:"0.07em" }}>Categorias</h3>
              <div style={{ display:"flex", flexDirection:"column", gap:"0.2rem" }}>
                <button style={btnCatStyle(categoria === "")} onClick={() => filtrarCategoria("")}>🗂 Todas</button>
                {CATEGORIAS.map(cat => (
                  <button key={cat.slug} style={btnCatStyle(categoria === cat.slug)} onClick={() => filtrarCategoria(cat.slug)}>
                    {cat.icon} {cat.label}
                  </button>
                ))}
              </div>
            </div>
          </aside>

          {/* Grade */}
          <div>
            <div style={{ display:"flex", alignItems:"center", gap:"0.5rem", flexWrap:"wrap", marginBottom:"1.25rem" }}>
              <span style={{ fontSize:"0.85rem", color:"#64748b", fontWeight:600 }}>Ordenar:</span>
              {[["","Relevância"],["preco-asc","Menor Preço"],["preco-desc","Maior Preço"],["az","A→Z"],["za","Z→A"]].map(([k,l]) => (
                <button key={k} onClick={() => filtrarSort(k)} style={{ padding:"0.4rem 0.9rem", borderRadius:100, border:"1.5px solid "+(sort===k?"#7c3aed":"#e5e4f5"), background:sort===k?"#ede9fe":"#fff", color:sort===k?"#7c3aed":"#64748b", fontSize:"0.82rem", fontWeight:600, cursor:"pointer", transition:"all .18s" }}>{l}</button>
              ))}
            </div>
            <p style={{ color:"#64748b", fontSize:"0.86rem", marginBottom:"0.75rem" }}>{lista.length} produto(s) encontrado(s)</p>
            {lista.length > 0 ? (
              <div key={animKey} className="produtos-grid" style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(210px,1fr))", gap:"1.25rem" }}>
                {lista.map(p => <ProdutoCard key={p.id} produto={p} />)}
              </div>
            ) : (
              <div key={animKey} className="produtos-grid" style={{ textAlign:"center", padding:"4rem 2rem" }}>
                <div style={{ fontSize:"3.5rem", marginBottom:"1rem" }}>🔍</div>
                <h3 style={{ fontSize:"1.25rem", fontWeight:700, marginBottom:"0.5rem" }}>Nenhum produto encontrado</h3>
                <p style={{ color:"#64748b", marginBottom:"1.5rem" }}>Tente outros termos ou categorias.</p>
                <button onClick={limpar} style={{ padding:"0.6rem 1.25rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, border:"none", cursor:"pointer" }}>Ver Todos</button>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Detalhe do Produto ────────────────────────────────────────────────────────
function ProdutoDetalhe({ id }) {
  const produto   = PRODUTOS.find(p => p.id === parseInt(id));
  const { addItem }   = useCart();
  const { showToast } = useToast();
  const [qty, setQty]             = useState(1);
  const [adicionado, setAdicionado] = useState(false);
  const [imgErro, setImgErro]     = useState(false);

  if (!produto) return (
    <div style={{ textAlign:"center", padding:"4rem 2rem" }}>
      <div style={{ fontSize:"3.5rem", marginBottom:"1rem" }}>😕</div>
      <h3 style={{ fontSize:"1.25rem", fontWeight:700, marginBottom:"1rem" }}>Produto não encontrado</h3>
      <a href="#/produtos" style={{ padding:"0.6rem 1.25rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, textDecoration:"none", display:"inline-block" }}>Ver Produtos</a>
    </div>
  );

  const relacionados = PRODUTOS.filter(p => p.categoria === produto.categoria && p.id !== produto.id).slice(0, 4);
  const descPct      = produto.preco_antigo ? descontoPct(produto.preco, produto.preco_antigo) : 0;
  const icon         = CAT_ICONS[produto.categoria] || "📦";

  function handleAdd() {
    addItem(produto, qty);
    setAdicionado(true);
    showToast("✓ " + produto.nome + " adicionado ao carrinho!");
    setTimeout(() => setAdicionado(false), 2000);
  }

  const estoqueEl =
    produto.estoque > 10 ? <span style={{ color:"#16a34a", fontWeight:600, fontSize:"0.9rem" }}>✓ Em estoque ({produto.estoque} unidades)</span>
    : produto.estoque > 0 ? <span style={{ color:"#d97706", fontWeight:600, fontSize:"0.9rem" }}>⚠ Últimas {produto.estoque} unidades!</span>
    : <span style={{ color:"#dc2626", fontWeight:600, fontSize:"0.9rem" }}>✗ Fora de estoque</span>;

  return (
    <div>
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
        {/* Breadcrumb */}
        <div style={{ padding:"1.25rem 0", fontSize:"0.84rem", color:"#64748b" }}>
          <a href="#/" style={{ color:"#64748b", textDecoration:"none" }}>Início</a> /&nbsp;
          <a href="#/produtos" style={{ color:"#64748b", textDecoration:"none" }}>Produtos</a> /&nbsp;
          <a href={"#/produtos?categoria=" + produto.categoria} style={{ color:"#64748b", textDecoration:"none" }}>
            {produto.categoria.charAt(0).toUpperCase() + produto.categoria.slice(1)}
          </a> /&nbsp;
          <span style={{ color:"#1a1a2e", fontWeight:600 }}>{produto.nome}</span>
        </div>

        {/* Imagem + Info */}
        <div style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"3rem", marginBottom:"3rem", background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"2rem" }}>
          <div>
            <div style={{ width:"100%", paddingBottom:"100%", position:"relative", background:"#f8f7ff", borderRadius:12, overflow:"hidden" }}>
              {!imgErro ? (
                <img src={produto.imagemUrl} alt={produto.nome} onError={() => setImgErro(true)}
                  style={{ position:"absolute", inset:0, width:"100%", height:"100%", objectFit:"cover", objectPosition:"center", display:"block", transition:"transform .4s" }}
                  onMouseEnter={e => e.target.style.transform = "scale(1.03)"}
                  onMouseLeave={e => e.target.style.transform = "scale(1)"}
                />
              ) : (
                <div style={{ position:"absolute", inset:0, display:"flex", alignItems:"center", justifyContent:"center", background:"linear-gradient(135deg,#ede9fe,#f5f3ff)", fontSize:"5rem" }}>{icon}</div>
              )}
            </div>
          </div>
          <div>
            <span style={{ display:"inline-block", background:"#ede9fe", color:"#7c3aed", padding:"0.25rem 0.85rem", borderRadius:100, fontSize:"0.78rem", fontWeight:700, marginBottom:"0.75rem" }}>{produto.marca}</span>
            <h1 style={{ fontSize:"1.7rem", fontWeight:800, marginBottom:"0.75rem" }}>{produto.nome}</h1>
            <div style={{ fontSize:"0.9rem", color:"#f59e0b", marginBottom:"1rem" }}>
              {estrelas(produto.rating)} <span style={{ color:"#64748b" }}>{produto.rating} / 5.0</span>
            </div>
            <div style={{ marginBottom:"1.25rem" }}>
              {produto.preco_antigo && (
                <div style={{ display:"flex", alignItems:"center", gap:"0.5rem" }}>
                  <span style={{ fontSize:"0.95rem", color:"#64748b", textDecoration:"line-through" }}>{fmtPreco(produto.preco_antigo)}</span>
                  <span style={{ background:"#f43f5e", color:"#fff", fontSize:"0.78rem", fontWeight:700, padding:"0.2rem 0.55rem", borderRadius:6 }}>-{descPct}% OFF</span>
                </div>
              )}
              <p style={{ fontSize:"2.2rem", fontWeight:900, color:"#1a1a2e" }}>{fmtPreco(produto.preco)}</p>
              <p style={{ fontSize:"0.85rem", color:"#64748b" }}>ou 12x de {fmtPreco(produto.preco / 12)} sem juros</p>
            </div>
            <p style={{ color:"#64748b", lineHeight:1.75, marginBottom:"1.25rem", fontSize:"0.95rem" }}>{produto.descricao}</p>
            <div style={{ marginBottom:"1.25rem" }}>{estoqueEl}</div>
            <div style={{ display:"flex", alignItems:"center", gap:"1rem", marginBottom:"1.25rem" }}>
              <span style={{ fontSize:"0.9rem", fontWeight:600 }}>Quantidade:</span>
              <div style={{ display:"flex", alignItems:"center", gap:"0.5rem" }}>
                <button onClick={() => setQty(v => Math.max(1, v - 1))} style={{ width:36, height:36, border:"1.5px solid #e5e4f5", borderRadius:9, background:"#fff", cursor:"pointer", fontSize:"1.1rem" }}>−</button>
                <span style={{ width:52, height:36, display:"flex", alignItems:"center", justifyContent:"center", border:"1.5px solid #e5e4f5", borderRadius:9, fontWeight:700 }}>{qty}</span>
                <button onClick={() => setQty(v => Math.min(produto.estoque, v + 1))} style={{ width:36, height:36, border:"1.5px solid #e5e4f5", borderRadius:9, background:"#fff", cursor:"pointer", fontSize:"1.1rem" }}>+</button>
              </div>
            </div>
            <div style={{ display:"flex", gap:"0.75rem", marginBottom:"1.25rem", flexWrap:"wrap" }}>
              <button onClick={handleAdd} disabled={produto.estoque === 0} style={{ display:"flex", alignItems:"center", gap:"0.5rem", padding:"0.85rem 1.85rem", borderRadius:10, fontWeight:600, fontSize:"1rem", background:adicionado?"#16a34a":"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", border:"none", cursor:produto.estoque===0?"not-allowed":"pointer", opacity:produto.estoque===0?.5:1, transition:"all .2s" }}>
                {adicionado ? "✓ Adicionado" : (produto.estoque === 0 ? "Fora de Estoque" : "🛒 Adicionar ao Carrinho")}
              </button>
              <a href="#/carrinho" style={{ display:"inline-flex", alignItems:"center", gap:"0.5rem", padding:"0.85rem 1.85rem", borderRadius:10, fontWeight:600, fontSize:"1rem", color:"#7c3aed", border:"2px solid #7c3aed", textDecoration:"none" }}>Ver Carrinho</a>
            </div>
            <div style={{ display:"flex", flexWrap:"wrap", gap:"0.5rem" }}>
              {[produto.categoria.charAt(0).toUpperCase() + produto.categoria.slice(1), produto.marca, "Garantia 12 meses", "Frete Grátis"].map(t => (
                <span key={t} style={{ padding:"0.3rem 0.75rem", border:"1px solid #e5e4f5", borderRadius:100, fontSize:"0.78rem", color:"#64748b" }}>{t}</span>
              ))}
            </div>
          </div>
        </div>

        {relacionados.length > 0 && (
          <section style={{ padding:"2rem 0 3rem" }}>
            <h2 style={{ fontSize:"1.5rem", fontWeight:800, marginBottom:"1.5rem" }}>Produtos Relacionados</h2>
            <div style={{ display:"grid", gridTemplateColumns:"repeat(auto-fill,minmax(220px,1fr))", gap:"1.25rem" }}>
              {relacionados.map(p => <ProdutoCard key={p.id} produto={p} />)}
            </div>
          </section>
        )}
      </div>
    </div>
  );
}

// ── Carrinho ──────────────────────────────────────────────────────────────────
function Carrinho() {
  const { items, totalItems, totalValor, removeItem, updateQty, clearCart } = useCart();
  const { usuario } = useAuth();

  function finalizar() {
    const id = "ERA-" + Date.now();
    clearCart();
    navegar("/pedido-confirmado/" + id);
  }

  const cabecalho = (
    <div style={{ background:"linear-gradient(135deg,#1a1a2e,#2e1065)", color:"#fff", padding:"2.75rem 0", marginBottom:"2rem" }}>
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem" }}>
        <h1 style={{ fontSize:"2rem", fontWeight:800 }}>Meu Carrinho</h1>
      </div>
    </div>
  );

  if (items.length === 0) return (
    <div>
      {cabecalho}
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem 4rem", textAlign:"center" }}>
        <div style={{ fontSize:"3.5rem", marginBottom:"1rem" }}>🛒</div>
        <h3 style={{ fontSize:"1.25rem", fontWeight:700, marginBottom:"0.5rem" }}>Seu carrinho está vazio</h3>
        <p style={{ color:"#64748b", marginBottom:"1.5rem" }}>Adicione produtos para continuar.</p>
        <a href="#/produtos" style={{ display:"inline-flex", padding:"0.85rem 1.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"1rem", textDecoration:"none" }}>Ver Produtos</a>
      </div>
    </div>
  );

  return (
    <div>
      {cabecalho}
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem 4rem" }}>
        <div style={{ display:"grid", gridTemplateColumns:"1fr 340px", gap:"2rem" }}>
          <div>
            <h2 style={{ fontSize:"1.25rem", fontWeight:700, marginBottom:"1rem" }}>Itens ({totalItems})</h2>
            {items.map(item => (
              <div key={item.produto_id} style={{ display:"grid", gridTemplateColumns:"88px 1fr auto", gap:"1rem", alignItems:"center", background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"1rem", marginBottom:"0.75rem" }}>
                <div style={{ width:88, height:88, borderRadius:10, overflow:"hidden", background:"#f8f7ff", flexShrink:0 }}>
                  <img src={item.imagemUrl} alt={item.nome} style={{ width:"100%", height:"100%", objectFit:"cover", objectPosition:"center", display:"block" }} />
                </div>
                <div>
                  <p style={{ fontSize:"0.72rem", color:"#7c3aed", fontWeight:700, textTransform:"uppercase", marginBottom:"0.15rem" }}>{item.marca}</p>
                  <p style={{ fontWeight:700, fontSize:"0.9rem", marginBottom:"0.25rem" }}>{item.nome}</p>
                  <p style={{ fontSize:"0.85rem", color:"#64748b" }}>{fmtPreco(item.preco)} cada</p>
                </div>
                <div style={{ display:"flex", flexDirection:"column", alignItems:"flex-end", gap:"0.5rem" }}>
                  <div style={{ display:"flex", alignItems:"center", gap:"0.4rem" }}>
                    <button onClick={() => updateQty(item.produto_id, item.quantidade - 1)} style={{ width:30, height:30, border:"1.5px solid #e5e4f5", borderRadius:7, background:"#fff", cursor:"pointer", fontSize:"1rem" }}>−</button>
                    <span style={{ width:40, textAlign:"center", fontWeight:700, fontSize:"0.95rem" }}>{item.quantidade}</span>
                    <button onClick={() => updateQty(item.produto_id, item.quantidade + 1)} style={{ width:30, height:30, border:"1.5px solid #e5e4f5", borderRadius:7, background:"#fff", cursor:"pointer", fontSize:"1rem" }}>+</button>
                  </div>
                  <p style={{ fontWeight:800, fontSize:"1rem", color:"#6d28d9" }}>{fmtPreco(item.preco * item.quantidade)}</p>
                  <button onClick={() => removeItem(item.produto_id)} style={{ background:"none", border:"none", cursor:"pointer", color:"#64748b", padding:"0.35rem", borderRadius:7, fontSize:"1.1rem" }}
                    onMouseEnter={e => { e.currentTarget.style.color = "#dc2626"; e.currentTarget.style.background = "#fee2e2"; }}
                    onMouseLeave={e => { e.currentTarget.style.color = "#64748b"; e.currentTarget.style.background = "none"; }}>
                    🗑
                  </button>
                </div>
              </div>
            ))}
          </div>
          <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"1.5rem", position:"sticky", top:80, alignSelf:"start" }}>
            <h2 style={{ fontSize:"1.05rem", fontWeight:700, marginBottom:"1.25rem" }}>Resumo do Pedido</h2>
            <div style={{ display:"flex", justifyContent:"space-between", padding:"0.6rem 0", fontSize:"0.9rem", borderBottom:"1px solid #e5e4f5" }}><span>Subtotal ({totalItems} itens)</span><span>{fmtPreco(totalValor)}</span></div>
            <div style={{ display:"flex", justifyContent:"space-between", padding:"0.6rem 0", fontSize:"0.9rem", borderBottom:"1px solid #e5e4f5" }}><span>Frete</span><span style={{ color:"#16a34a", fontWeight:700 }}>Grátis ✓</span></div>
            <div style={{ display:"flex", justifyContent:"space-between", padding:"0.6rem 0", fontSize:"1.05rem", fontWeight:800 }}><span>Total à vista</span><span>{fmtPreco(totalValor)}</span></div>
            <p style={{ fontSize:"0.78rem", color:"#64748b", marginBottom:"1.25rem", marginTop:"0.5rem" }}>ou 12x de {fmtPreco(totalValor / 12)} sem juros</p>
            {usuario
              ? <button onClick={finalizar} style={{ width:"100%", padding:"0.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"1rem", border:"none", cursor:"pointer", marginBottom:"0.6rem" }}>✓ Finalizar Compra</button>
              : <a href="#/login" style={{ display:"block", padding:"0.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"1rem", textDecoration:"none", textAlign:"center", marginBottom:"0.6rem" }}>Fazer Login para Comprar</a>
            }
            <a href="#/produtos" style={{ display:"block", padding:"0.85rem", borderRadius:10, border:"2px solid #7c3aed", color:"#7c3aed", fontWeight:600, fontSize:"1rem", textDecoration:"none", textAlign:"center" }}>Continuar Comprando</a>
          </div>
        </div>
      </div>
    </div>
  );
}

// ── Login ─────────────────────────────────────────────────────────────────────
function Login() {
  const { login }      = useAuth();
  const { showToast }  = useToast();
  const [email, setEmail]               = useState("");
  const [senha, setSenha]               = useState("");
  const [mostrarSenha, setMostrarSenha] = useState(false);
  const [carregando, setCarregando]     = useState(false);
  const [erro, setErro]                 = useState("");

  async function entrar(e) {
    e.preventDefault();
    setErro(""); setCarregando(true);
    await new Promise(r => setTimeout(r, 500));
    const u = DEMO_USERS[email.toLowerCase()];
    if (u && u.senha === senha) {
      login({ nome:u.nome, email:email.toLowerCase(), telefone:u.telefone, endereco:u.endereco, cpf:u.cpf });
      showToast("✓ Bem-vindo(a) de volta, " + u.nome + "!");
      navegar("/");
    } else {
      setErro("E-mail ou senha incorretos. Use joao@email.com ou maria@email.com com senha 123456.");
    }
    setCarregando(false);
  }

  const inputStyle = { width:"100%", padding:"0.75rem 0.95rem", border:"1.5px solid #e5e4f5", borderRadius:10, fontSize:"0.9rem", boxSizing:"border-box", outline:"none" };

  return (
    <div style={{ minHeight:"calc(100vh - 66px)", display:"flex", alignItems:"center", justifyContent:"center", background:"linear-gradient(135deg,#f5f3ff,#ede9fe)", padding:"2rem" }}>
      <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:20, padding:"2.75rem 2.5rem", width:"100%", maxWidth:420, boxShadow:"0 8px 32px rgba(124,58,237,.12)", animation:"cardEntrada .4s cubic-bezier(.4,0,.2,1) both" }}>
        <div style={{ textAlign:"center", marginBottom:"2rem" }}>
          <div style={{ width:58, height:58, borderRadius:16, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", display:"inline-flex", alignItems:"center", justifyContent:"center", marginBottom:"1rem", boxShadow:"0 6px 20px rgba(124,58,237,.4)", animation:"iconPulso .6s ease .3s both", fontSize:"1.5rem" }}>⚡</div>
          <h1 style={{ fontSize:"1.55rem", fontWeight:800, marginBottom:"0.3rem" }}>Bem-vindo de volta!</h1>
          <p style={{ color:"#64748b", fontSize:"0.9rem" }}>Entre na sua conta Nova E.R.A.</p>
        </div>
        <div style={{ background:"#ede9fe", borderRadius:12, padding:"0.85rem 1rem", marginBottom:"1.5rem", fontSize:"0.82rem", color:"#6d28d9", lineHeight:1.6, animation:"campoEntrada .4s ease .15s both" }}>
          <strong>Contas para testar:</strong><br />joao@email.com / 123456<br />maria@email.com / 123456
        </div>
        <form onSubmit={entrar} style={{ display:"flex", flexDirection:"column", gap:"1rem" }}>
          <div style={{ animation:"campoEntrada .4s ease .2s both" }}>
            <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>E-mail</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required autoFocus placeholder="seu@email.com" style={inputStyle} />
          </div>
          <div style={{ animation:"campoEntrada .4s ease .27s both" }}>
            <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>Senha</label>
            <div style={{ position:"relative" }}>
              <input type={mostrarSenha?"text":"password"} value={senha} onChange={e => setSenha(e.target.value)} required placeholder="••••••" style={{ ...inputStyle, paddingRight:"2.75rem" }} />
              <button type="button" onClick={() => setMostrarSenha(v => !v)} style={{ position:"absolute", right:"0.75rem", top:"50%", transform:"translateY(-50%)", background:"none", border:"none", cursor:"pointer", color:"#94a3b8", fontSize:"1rem" }}>{mostrarSenha ? "🙈" : "👁"}</button>
            </div>
          </div>
          {erro && <div style={{ background:"#fee2e2", borderRadius:10, padding:"0.75rem 1rem", color:"#dc2626", fontSize:"0.84rem", animation:"erroEntrada .25s ease" }}>{erro}</div>}
          <button type="submit" disabled={carregando} style={{ padding:"0.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:700, fontSize:"1rem", border:"none", cursor:"pointer", opacity:carregando?.75:1, animation:"campoEntrada .4s ease .35s both" }}>
            {carregando ? "Entrando..." : "Entrar"}
          </button>
        </form>
        <p style={{ textAlign:"center", marginTop:"1.5rem", fontSize:"0.88rem", color:"#64748b" }}>
          Não tem conta? <a href="#/cadastro" style={{ color:"#7c3aed", fontWeight:700, textDecoration:"none" }}>Criar Conta</a>
        </p>
      </div>
    </div>
  );
}

// ── Cadastro ──────────────────────────────────────────────────────────────────
function Cadastro() {
  const { login }      = useAuth();
  const { showToast }  = useToast();
  const [nome, setNome]                   = useState("");
  const [email, setEmail]                 = useState("");
  const [senha, setSenha]                 = useState("");
  const [confirmacao, setConfirmacao]     = useState("");
  const [mostrarSenha, setMostrarSenha]   = useState(false);
  const [carregando, setCarregando]       = useState(false);
  const [erro, setErro]                   = useState("");

  async function criarConta(e) {
    e.preventDefault();
    setErro("");
    if (senha.length < 6)      { setErro("A senha deve ter pelo menos 6 caracteres."); return; }
    if (senha !== confirmacao)  { setErro("As senhas não coincidem."); return; }
    setCarregando(true);
    await new Promise(r => setTimeout(r, 600));
    login({ nome, email });
    showToast("✓ Conta criada! Bem-vindo(a), " + nome + "!");
    navegar("/");
    setCarregando(false);
  }

  const inputStyle = { width:"100%", padding:"0.75rem 0.95rem", border:"1.5px solid #e5e4f5", borderRadius:10, fontSize:"0.9rem", boxSizing:"border-box", outline:"none" };

  return (
    <div style={{ minHeight:"calc(100vh - 66px)", display:"flex", alignItems:"center", justifyContent:"center", background:"linear-gradient(135deg,#f5f3ff,#ede9fe)", padding:"2rem" }}>
      <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:20, padding:"2.75rem 2.5rem", width:"100%", maxWidth:420, boxShadow:"0 8px 32px rgba(124,58,237,.12)", animation:"cardEntrada .4s cubic-bezier(.4,0,.2,1) both" }}>
        <div style={{ textAlign:"center", marginBottom:"2rem" }}>
          <div style={{ width:58, height:58, borderRadius:16, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", display:"inline-flex", alignItems:"center", justifyContent:"center", marginBottom:"1rem", boxShadow:"0 6px 20px rgba(124,58,237,.4)", animation:"iconPulso .6s ease .3s both", fontSize:"1.5rem" }}>⚡</div>
          <h1 style={{ fontSize:"1.55rem", fontWeight:800, marginBottom:"0.3rem" }}>Criar Conta</h1>
          <p style={{ color:"#64748b", fontSize:"0.9rem" }}>Junte-se à Nova E.R.A. hoje mesmo!</p>
        </div>
        <form onSubmit={criarConta} style={{ display:"flex", flexDirection:"column", gap:"1rem" }}>
          <div style={{ animation:"campoEntrada .4s ease .15s both" }}>
            <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>Nome Completo</label>
            <input type="text" value={nome} onChange={e => setNome(e.target.value)} required autoFocus placeholder="João Silva" style={inputStyle} />
          </div>
          <div style={{ animation:"campoEntrada .4s ease .22s both" }}>
            <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>E-mail</label>
            <input type="email" value={email} onChange={e => setEmail(e.target.value)} required placeholder="seu@email.com" style={inputStyle} />
          </div>
          <div style={{ animation:"campoEntrada .4s ease .29s both" }}>
            <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>Senha</label>
            <div style={{ position:"relative" }}>
              <input type={mostrarSenha?"text":"password"} value={senha} onChange={e => setSenha(e.target.value)} required placeholder="Mínimo 6 caracteres" style={{ ...inputStyle, paddingRight:"2.75rem" }} />
              <button type="button" onClick={() => setMostrarSenha(v => !v)} style={{ position:"absolute", right:"0.75rem", top:"50%", transform:"translateY(-50%)", background:"none", border:"none", cursor:"pointer", color:"#94a3b8", fontSize:"1rem" }}>{mostrarSenha ? "🙈" : "👁"}</button>
            </div>
          </div>
          <div style={{ animation:"campoEntrada .4s ease .36s both" }}>
            <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>Confirmar Senha</label>
            <input type={mostrarSenha?"text":"password"} value={confirmacao} onChange={e => setConfirmacao(e.target.value)} required placeholder="••••••" style={inputStyle} />
          </div>
          {erro && <div style={{ background:"#fee2e2", borderRadius:10, padding:"0.75rem 1rem", color:"#dc2626", fontSize:"0.84rem", animation:"erroEntrada .25s ease" }}>{erro}</div>}
          <button type="submit" disabled={carregando} style={{ padding:"0.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:700, fontSize:"1rem", border:"none", cursor:"pointer", opacity:carregando?.75:1, marginTop:"0.25rem", animation:"campoEntrada .4s ease .43s both" }}>
            {carregando ? "Criando conta..." : "Criar Conta"}
          </button>
        </form>
        <p style={{ textAlign:"center", marginTop:"1.5rem", fontSize:"0.88rem", color:"#64748b" }}>
          Já tem conta? <a href="#/login" style={{ color:"#7c3aed", fontWeight:700, textDecoration:"none" }}>Entrar</a>
        </p>
      </div>
    </div>
  );
}

// ── Perfil ────────────────────────────────────────────────────────────────────
function Perfil({ params }) {
  const { usuario, logout, updateUser } = useAuth();
  const { showToast } = useToast();
  const [aba, setAba]           = useState(params.get("tab") === "pedidos" ? "pedidos" : "perfil");
  const [nome, setNome]         = useState(usuario?.nome || "");
  const [email, setEmail]       = useState(usuario?.email || "");
  const [telefone, setTelefone] = useState(usuario?.telefone || "");
  const [endereco, setEndereco] = useState(usuario?.endereco || "");
  const [cpf, setCpf]           = useState(usuario?.cpf || "");
  const [salvando, setSalvando] = useState(false);

  if (!usuario) return (
    <div style={{ minHeight:"calc(100vh - 66px)", display:"flex", alignItems:"center", justifyContent:"center" }}>
      <div style={{ textAlign:"center" }}>
        <div style={{ fontSize:"3.5rem", marginBottom:"1rem" }}>🔒</div>
        <h3 style={{ fontSize:"1.25rem", fontWeight:700, marginBottom:"0.5rem" }}>Área Restrita</h3>
        <p style={{ color:"#64748b", marginBottom:"1.5rem" }}>Faça login para acessar seu perfil.</p>
        <a href="#/login" style={{ padding:"0.85rem 1.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, textDecoration:"none" }}>Fazer Login</a>
      </div>
    </div>
  );

  async function salvar(e) {
    e.preventDefault();
    setSalvando(true);
    await new Promise(r => setTimeout(r, 600));
    updateUser({ nome, email, telefone, endereco, cpf });
    showToast("✓ Perfil atualizado com sucesso!");
    setSalvando(false);
  }

  const tabStyle = (ativo) => ({
    display:"flex", alignItems:"center", gap:"0.5rem",
    padding:"0.65rem 1.25rem", borderRadius:10, fontSize:"0.9rem",
    background: ativo ? "#ede9fe" : "transparent",
    color:      ativo ? "#7c3aed" : "#64748b",
    fontWeight: ativo ? 700       : 500,
    cursor:"pointer", border:"none", transition:"all .2s",
  });

  const inputStyle = { width:"100%", padding:"0.75rem 0.95rem", border:"1.5px solid #e5e4f5", borderRadius:10, fontSize:"0.9rem", boxSizing:"border-box", outline:"none" };

  const pedidosExemplo = [
    { id:"ERA-001", data:"15/03/2026", status:"Entregue",    total:8999.99, itens:["iPhone 15 Pro Max x1"] },
    { id:"ERA-002", data:"28/03/2026", status:"Em trânsito", total:1999.99, itens:["Sony WH-1000XM5 x1"] },
  ];

  return (
    <div>
      <div style={{ background:"linear-gradient(135deg,#1a1a2e,#2e1065)", color:"#fff", padding:"2.75rem 0", marginBottom:"2rem" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem", display:"flex", alignItems:"center", gap:"1.25rem" }}>
          <div style={{ width:72, height:72, borderRadius:"50%", background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", display:"flex", alignItems:"center", justifyContent:"center", fontSize:"1.8rem" }}>👤</div>
          <div>
            <h1 style={{ fontSize:"1.8rem", fontWeight:800 }}>{usuario.nome}</h1>
            <p style={{ color:"#a78bfa", marginTop:"0.2rem" }}>{usuario.email}</p>
          </div>
        </div>
      </div>
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem 4rem" }}>
        <div style={{ display:"grid", gridTemplateColumns:"200px 1fr", gap:"2rem" }}>
          <aside>
            <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"0.75rem" }}>
              <button style={tabStyle(aba === "perfil")}  onClick={() => setAba("perfil")}>👤 Meu Perfil</button>
              <button style={tabStyle(aba === "pedidos")} onClick={() => setAba("pedidos")}>📦 Pedidos</button>
              <div style={{ borderTop:"1px solid #e5e4f5", marginTop:"0.5rem", paddingTop:"0.5rem" }}>
                <button style={{ ...tabStyle(false), color:"#dc2626" }} onClick={() => { logout(); navegar("/"); }}>↩ Sair</button>
              </div>
            </div>
          </aside>
          <main>
            {aba === "perfil" ? (
              <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"2rem" }}>
                <h2 style={{ fontSize:"1.2rem", fontWeight:700, marginBottom:"1.5rem" }}>Dados Pessoais</h2>
                <form onSubmit={salvar} style={{ display:"grid", gridTemplateColumns:"1fr 1fr", gap:"1rem" }}>
                  {[
                    { label:"Nome Completo", value:nome,     setter:setNome,     type:"text",  placeholder:"João Silva",         full:true },
                    { label:"E-mail",        value:email,    setter:setEmail,    type:"email", placeholder:"seu@email.com",       full:true },
                    { label:"Telefone",      value:telefone, setter:setTelefone, type:"text",  placeholder:"(11) 98765-4321" },
                    { label:"CPF",           value:cpf,      setter:setCpf,      type:"text",  placeholder:"000.000.000-00" },
                    { label:"Endereço",      value:endereco, setter:setEndereco, type:"text",  placeholder:"Rua, nº - Cidade/UF", full:true },
                  ].map(({ label, value, setter, type, placeholder, full }) => (
                    <div key={label} style={{ gridColumn: full ? "1 / -1" : undefined }}>
                      <label style={{ display:"block", fontSize:"0.85rem", fontWeight:600, marginBottom:"0.35rem" }}>{label}</label>
                      <input type={type} value={value} onChange={e => setter(e.target.value)} placeholder={placeholder} style={inputStyle} />
                    </div>
                  ))}
                  <div style={{ gridColumn:"1 / -1", display:"flex", justifyContent:"flex-end" }}>
                    <button type="submit" disabled={salvando} style={{ padding:"0.85rem 2rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"0.95rem", border:"none", cursor:"pointer", opacity:salvando?.7:1 }}>
                      {salvando ? "Salvando..." : "Salvar Alterações"}
                    </button>
                  </div>
                </form>
              </div>
            ) : (
              <div>
                <h2 style={{ fontSize:"1.2rem", fontWeight:700, marginBottom:"1.25rem" }}>Meus Pedidos</h2>
                {pedidosExemplo.map(o => (
                  <div key={o.id} style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"1.5rem", marginBottom:"1rem" }}>
                    <div style={{ display:"flex", alignItems:"center", justifyContent:"space-between", marginBottom:"0.75rem" }}>
                      <div>
                        <p style={{ fontSize:"0.9rem", fontWeight:700, marginBottom:"0.2rem" }}>Pedido #{o.id}</p>
                        <p style={{ color:"#64748b", fontSize:"0.82rem" }}>Realizado em {o.data}</p>
                      </div>
                      <div style={{ textAlign:"right" }}>
                        <span style={{ display:"inline-block", background:o.status==="Entregue"?"#dcfce7":"#ede9fe", color:o.status==="Entregue"?"#16a34a":"#7c3aed", padding:"0.3rem 0.85rem", borderRadius:100, fontSize:"0.78rem", fontWeight:700 }}>{o.status}</span>
                        <p style={{ fontWeight:800, marginTop:"0.35rem" }}>{fmtPreco(o.total)}</p>
                      </div>
                    </div>
                    <div style={{ fontSize:"0.86rem", color:"#64748b" }}>
                      {o.itens.map(i => <span key={i} style={{ display:"block" }}>• {i}</span>)}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </main>
        </div>
      </div>
    </div>
  );
}

// ── Sobre ─────────────────────────────────────────────────────────────────────
function Sobre() {
  const valores = [
    { icon:"⚡", titulo:"Inovação",   desc:"Sempre os lançamentos mais recentes e as tecnologias de ponta." },
    { icon:"👥", titulo:"Comunidade", desc:"Uma equipe dedicada e clientes que confiam em nós há anos." },
    { icon:"🏆", titulo:"Qualidade",  desc:"Apenas produtos originais com garantia de fábrica." },
    { icon:"❤️", titulo:"Paixão",     desc:"Apaixonados por tecnologia e pelo melhor atendimento ao cliente." },
  ];
  return (
    <div>
      <div style={{ background:"linear-gradient(135deg,#1a1a2e,#2e1065)", color:"#fff", padding:"4rem 0", marginBottom:"3rem" }}>
        <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem", textAlign:"center" }}>
          <div style={{ width:72, height:72, borderRadius:18, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", display:"flex", alignItems:"center", justifyContent:"center", margin:"0 auto 1.25rem", boxShadow:"0 4px 16px rgba(124,58,237,.4)", fontSize:"2rem" }}>⚡</div>
          <h1 style={{ fontSize:"2.5rem", fontWeight:800, marginBottom:"1rem" }}><span style={{ color:"#fff" }}>Nova</span><span style={{ color:"#a78bfa" }}>E.R.A.</span></h1>
          <p style={{ color:"#a78bfa", fontSize:"1.1rem", maxWidth:520, margin:"0 auto" }}>A loja de eletrônicos que redefine sua experiência de compra no Brasil.</p>
        </div>
      </div>
      <div style={{ maxWidth:1200, margin:"0 auto", padding:"0 1.5rem 4rem" }}>
        <div style={{ background:"#fff", border:"1px solid #e5e4f5", borderRadius:20, padding:"2.5rem", marginBottom:"2rem" }}>
          <h2 style={{ fontSize:"1.5rem", fontWeight:800, marginBottom:"1rem" }}>Nossa História</h2>
          <p style={{ color:"#64748b", lineHeight:1.8, fontSize:"0.97rem", marginBottom:"1rem" }}>Fundada em 2020, a Nova E.R.A. nasceu da paixão por tecnologia e do desejo de oferecer aos consumidores brasileiros acesso fácil e confiável aos melhores produtos eletrônicos do mundo. Com mais de 34 produtos catalogados em 8 categorias, somos referência em smartphones, notebooks, áudio, wearables, gaming e muito mais.</p>
          <p style={{ color:"#64748b", lineHeight:1.8, fontSize:"0.97rem" }}>Nossa missão é simples: conectar pessoas à tecnologia que transforma vidas, com preços justos, entrega rápida e atendimento excepcional.</p>
        </div>
        <div style={{ display:"grid", gridTemplateColumns:"repeat(4,1fr)", gap:"1.25rem", marginBottom:"2rem" }}>
          {[["34+","Produtos"],["8","Categorias"],["15+","Marcas"],["4.8★","Satisfação"]].map(([v,l]) => (
            <div key={l} style={{ background:"linear-gradient(135deg,#ede9fe,#f5f3ff)", border:"1px solid #e5e4f5", borderRadius:14, padding:"1.75rem", textAlign:"center" }}>
              <p style={{ fontSize:"2.5rem", fontWeight:900, color:"#7c3aed", marginBottom:"0.35rem" }}>{v}</p>
              <p style={{ color:"#64748b", fontSize:"0.88rem", fontWeight:600 }}>{l}</p>
            </div>
          ))}
        </div>
        <h2 style={{ fontSize:"1.5rem", fontWeight:800, marginBottom:"1.25rem" }}>Nossos Valores</h2>
        <div style={{ display:"grid", gridTemplateColumns:"repeat(2,1fr)", gap:"1.25rem", marginBottom:"2.5rem" }}>
          {valores.map((v, i) => (
            <div key={i} style={{ display:"flex", gap:"1.25rem", background:"#fff", border:"1px solid #e5e4f5", borderRadius:14, padding:"1.5rem", transition:"all .25s" }}
              onMouseEnter={e => { e.currentTarget.style.borderColor = "#7c3aed"; e.currentTarget.style.boxShadow = "0 4px 16px rgba(124,58,237,.12)"; }}
              onMouseLeave={e => { e.currentTarget.style.borderColor = "#e5e4f5"; e.currentTarget.style.boxShadow = ""; }}>
              <div style={{ fontSize:"1.75rem", flexShrink:0 }}>{v.icon}</div>
              <div>
                <h3 style={{ fontSize:"1rem", fontWeight:700, marginBottom:"0.35rem" }}>{v.titulo}</h3>
                <p style={{ color:"#64748b", fontSize:"0.87rem", lineHeight:1.6 }}>{v.desc}</p>
              </div>
            </div>
          ))}
        </div>
        <div style={{ textAlign:"center" }}>
          <h2 style={{ fontSize:"1.5rem", fontWeight:800, marginBottom:"0.75rem" }}>Pronto para explorar?</h2>
          <p style={{ color:"#64748b", marginBottom:"1.5rem" }}>Conheça nosso catálogo completo com os melhores eletrônicos do mercado.</p>
          <a href="#/produtos" style={{ display:"inline-flex", padding:"0.9rem 2rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"1rem", textDecoration:"none" }}>Ver Produtos</a>
        </div>
      </div>
    </div>
  );
}

// ── Pedido Confirmado ─────────────────────────────────────────────────────────
function PedidoConfirmado({ pedidoId }) {
  return (
    <div style={{ minHeight:"calc(100vh - 66px)", display:"flex", alignItems:"center", justifyContent:"center", padding:"2rem" }}>
      <div style={{ textAlign:"center", maxWidth:480, animation:"cardEntrada .5s ease" }}>
        <div style={{ fontSize:"5rem", marginBottom:"1.25rem" }}>🎉</div>
        <h1 style={{ fontSize:"2rem", fontWeight:800, marginBottom:"0.75rem" }}>Pedido Confirmado!</h1>
        <p style={{ color:"#64748b", marginBottom:"0.5rem", fontSize:"1rem" }}>Obrigado pela sua compra na Nova E.R.A.!</p>
        <p style={{ color:"#7c3aed", fontWeight:700, fontSize:"0.9rem", marginBottom:"2rem" }}>Pedido #{pedidoId}</p>
        <div style={{ background:"#f0fdf4", border:"1px solid #bbf7d0", borderRadius:14, padding:"1.5rem", marginBottom:"2rem", textAlign:"left" }}>
          {["✓ Pagamento confirmado","✓ Nota fiscal enviada por e-mail","✓ Entrega em até 5 dias úteis","✓ Rastreamento disponível em breve"].map(t => (
            <p key={t} style={{ color:"#16a34a", fontWeight:600, fontSize:"0.9rem", marginBottom:"0.35rem" }}>{t}</p>
          ))}
        </div>
        <div style={{ display:"flex", gap:"1rem", justifyContent:"center", flexWrap:"wrap" }}>
          <a href="#/" style={{ padding:"0.85rem 1.85rem", borderRadius:10, background:"linear-gradient(135deg,#7c3aed,#8b5cf6)", color:"#fff", fontWeight:600, fontSize:"1rem", textDecoration:"none" }}>Voltar ao Início</a>
          <a href="#/produtos" style={{ padding:"0.85rem 1.85rem", borderRadius:10, border:"2px solid #7c3aed", color:"#7c3aed", fontWeight:600, fontSize:"1rem", textDecoration:"none" }}>Continuar Comprando</a>
        </div>
      </div>
    </div>
  );
}

// =============================================================================
// 7. ROTEADOR PRINCIPAL — decide qual página renderizar com base no hash
// =============================================================================

function App() {
  const hash               = useHash();
  const { partes, params } = parsearHash(hash);
  const rota               = partes[0] || "";

  let pagina;
  if      (rota === "")                              pagina = <Home />;
  else if (rota === "produtos")                      pagina = <Produtos params={params} />;
  else if (rota === "produto"  && partes[1])         pagina = <ProdutoDetalhe id={partes[1]} />;
  else if (rota === "carrinho")                      pagina = <Carrinho />;
  else if (rota === "login")                         pagina = <Login />;
  else if (rota === "cadastro")                      pagina = <Cadastro />;
  else if (rota === "perfil")                        pagina = <Perfil params={params} />;
  else if (rota === "sobre")                         pagina = <Sobre />;
  else if (rota === "pedido-confirmado" && partes[1])pagina = <PedidoConfirmado pedidoId={partes[1]} />;
  else pagina = (
    <div style={{ textAlign:"center", padding:"4rem 2rem" }}>
      <div style={{ fontSize:"3.5rem", marginBottom:"1rem" }}>🔍</div>
      <h2 style={{ fontSize:"1.5rem", fontWeight:800, marginBottom:"0.5rem" }}>Página não encontrada</h2>
      <a href="#/" style={{ color:"#7c3aed", fontWeight:600, textDecoration:"none" }}>← Voltar ao início</a>
    </div>
  );

  return (
    <CartProvider>
      <AuthProvider>
        <ToastProvider>
          <div style={{ minHeight:"100vh", display:"flex", flexDirection:"column" }}>
            <Navbar />
            <main style={{ flex:1 }}>{pagina}</main>
            <Footer />
          </div>
        </ToastProvider>
      </AuthProvider>
    </CartProvider>
  );
}

// =============================================================================
// 8. INICIALIZAÇÃO — monta o React na div #root
// =============================================================================

ReactDOM.createRoot(document.getElementById("root")).render(<App />);
</script>
</body>
</html>"""
