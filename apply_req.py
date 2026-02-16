# -*- coding: utf-8 -*-
"""实现 req 红包特效 + 修复乱码"""
import re
path = r'd:\workspace\cursor_workspace\red_bag\index.html'
with open(path, 'r', encoding='utf-8', errors='replace') as f:
    c = f.read()

# 1. initRound: 添加 BLESSING_WORDS，money 包加 blessingWord
c = c.replace(
    "for (let i = 0; i < n; i++) {\n        if (types[i] === 'money') {\n          packets.push({ type: 'money', amount: amounts[amountIdx++], opened: false });",
    "const BLESSING_WORDS = ['\u65b0\u5e74\u5feb\u4e50','\u606d\u559c\u53d1\u8d22','\u9f99\u9a6c\u7cbe\u795e','\u4e07\u4e8b\u5982\u610f','\u8eab\u4f53\u5065\u5eb7'];\n      for (let i = 0; i < n; i++) {\n        if (types[i] === 'money') {\n          packets.push({ type: 'money', amount: amounts[amountIdx++], blessingWord: BLESSING_WORDS[Math.floor(Math.random()*5)], opened: false });"
)

# 2. renderPackets: money 显示 blessingWord + 金额；blessing 显示祝福字 + 文案
c = re.sub(
    r"if \(p\.type === 'money'\) \{\s+div\.innerHTML = `<span class=\"icon\">[^<]*</span><span class=\"amount\">[^`]*\$\{p\.amount\.toFixed\(2\)\}</span>`;",
    "if (p.type === 'money') {\n            div.innerHTML = `<span class=\"blessing-word\">${p.blessingWord || '\u606d\u559c\u53d1\u8d22'}</span><span class=\"amount\">\u00a5${p.amount.toFixed(2)}</span>`;",
    c, count=1
)
c = re.sub(
    r"} else if \(p\.type === 'blessing_health' \|\| p\.type === 'blessing_fortune'\) \{\s+div\.innerHTML = `<span class=\"icon\">[^<]*</span><span class=\"blessing\">\$\{p\.text\}</span>`;",
    "} else if (p.type === 'blessing_health' || p.type === 'blessing_fortune') {\n            div.innerHTML = `<span class=\"blessing-word\">${p.type === 'blessing_health' ? '龙马精神' : '恭喜发财'}</span><span class=\"blessing\">${p.text}</span>`;",
    c, count=1
)

# 3. 修复 emoji 乱码
c = c.replace('<span class="icon icon-mine">??</span>', '<span class="icon icon-mine">💣</span>')
c = c.replace('<span class="icon icon-firework">??</span>', '<span class="icon icon-firework">🎆</span>')
c = c.replace('<span class="icon icon-surprise">??</span>', '<span class="icon icon-surprise">🎁</span>')

# 4. blessing-word 样式
c = c.replace(
    '''    .packet .blessing {
      font-size: 0.8em;
      padding: 0 4px;
      text-align: center;
      color: #fff;
    }''',
    '''    .packet .blessing-word {
      font-size: 0.8em;
      color: var(--gold);
      font-weight: bold;
      margin-bottom: 2px;
      text-shadow: 0 0 6px rgba(255,215,0,0.8);
    }
    .packet .blessing {
      font-size: 0.75em;
      padding: 0 4px;
      text-align: center;
      color: rgba(255,255,255,0.95);
    }'''
)

# 5. 修复乱码
fixes = [
    ('<title>?????? - ????</title>', '<title>马年红包扫雷 - 新春快乐</title>'),
    ('/* ????? */', '/* 管理员面板 */'), ("content: '?';", "content: '福';"),
    ('title="???"', 'title="管理员"'), ('>?</button>\n  \n  <div class="container">', '>管</button>\n  \n  <div class="container">'),
    ('>? ??</button>', '>开 音乐</button>'), ('<h2>?????</h2>', '<h2>管理员面板</h2>'),
    ('placeholder="????????"', 'placeholder="请输入管理员密码"'),
    ('for="packetCount">????</label>', 'for="packetCount">红包个数</label>'),
    ('placeholder="?20"', 'placeholder="如20"'), ('6-50????1?+2??+2??', '6-50个，包含1雷+2礼花+2祝福'),
    ('for="totalAmount">????????</label>', 'for="totalAmount">预计总金额（元）</label>'),
    ('placeholder="?200"', 'placeholder="如200"'), ('???? = ??? / ??', '每局金额 = 总金额 / 局数'),
    ('for="roundCount">??</label>', 'for="roundCount">局数</label>'), ('placeholder="?10"', 'placeholder="如10"'),
    ('??? = ?? ? ??', '总局数 = 局数 × 每局'),
    ('id="startGameFromModal">????</button>', 'id="startGameFromModal">开始游戏</button>'),
    ('id="closeAdminModal" style="margin-top:8px">??</button>', 'id="closeAdminModal" style="margin-top:8px">关闭</button>'),
    ('<h1>??????</h1>', '<h1>马年红包扫雷</h1>'), ('id="startGame">????</button>', 'id="startGame">开始游戏</button>'),
    ("alert('??????6?');", "alert('红包个数至少6个');"),
    ("text: '?????????',", "text: '马年健康，龙马精神',"), ("text: '?????????',", "text: '马年发财，财源滚滚',"),
    ("toast.textContent = '????????????';", "toast.textContent = '亲，见好就收哦，小心踩雷';"),
    ("textContent = '?' +", "textContent = '¥' +"),
    ('<div class="modal-text">??????????????</div>', '<div class="modal-text">曹雨昕是世界上最美丽的女孩！</div>'),
    ('<div class="modal-text" style="margin-top:12px;font-size:1.1em">????????????</div>', '<div class="modal-text" style="margin-top:12px;font-size:1.1em">新的一年你会变得更漂亮！</div>'),
    ('<div class="modal-text" style="margin-top:8px;font-size:1.1em">??????????</div>', '<div class="modal-text" style="margin-top:8px;font-size:1.1em">你的光芒闪瞎我的眼！</div>'),
    ('style="margin-top:24px">???</button>', 'style="margin-top:24px">知道了</button>'),
    ('<div class="modal-text">????????</div>', '<div class="modal-text">到手的红包清空了</div>'),
    ('style="margin-top:20px">??</button>', 'style="margin-top:20px">确定</button>'),
    ('?????????? ?${roundAmount.toFixed(2)} ?</div>', '恭喜获得本局所有红包 ￥${roundAmount.toFixed(2)} 元</div>'),
    ('???? ?${totalAfter.toFixed(2)}</div>', '累计总额 ￥${totalAfter.toFixed(2)}</div>'),
    ('???? ?${totalAmount.toFixed(2)}</div>', '累计总额 ￥${totalAmount.toFixed(2)}</div>'),
    ('?? ?${amount.toFixed(2)}</div>', '获得 ￥${amount.toFixed(2)}</div>'),
    ('????????? ?${totalEarnedAmount.toFixed(2)}', '游戏结束，累计获得 ￥${totalEarnedAmount.toFixed(2)}'),
    ("const musicSrc = '?????.mp3';", "const musicSrc = '恭喜你发财.mp3';"),
]

# 精确替换 money innerHTML
c = re.sub(r'div\.innerHTML = `<span class="icon">[^<]*</span><span class="amount">[^`]*\$\{p\.amount\.toFixed\(2\)\}</span>`;\s*\n\s+} else if \(p\.type === \'blessing_health\'', 
    "div.innerHTML = `<span class=\"blessing-word\">${p.blessingWord || '恭喜发财'}</span><span class=\"amount\">¥${p.amount.toFixed(2)}</span>`;\n          } else if (p.type === 'blessing_health'", c, count=1)

c = c.replace("div.innerHTML = `<span class=\"icon\">福</span><span class=\"blessing\">${p.text}</span>`;",
              "div.innerHTML = `<span class=\"blessing-word\">${p.type === 'blessing_health' ? '\u9f99\u9a6c\u7cbe\u795e' : '\u606d\u559c\u53d1\u8d22'}</span><span class=\"blessing\">${p.text}</span>`;")

for old, new in fixes:
    c = c.replace(old, new)

# 其他可能乱码
c = c.replace('/* ?? */', '/* 标题 */', 1)
c = c.replace('/* ?? */', '/* 统计 */', 1)
c = c.replace('>?????</div>\n          <div class="value" id="currentAmount">', '>当前局获得</div>\n          <div class="value" id="currentAmount">')
c = c.replace('id="currentAmount">?0.00</div>', 'id="currentAmount">¥0.00</div>')
c = c.replace('>?????</div>\n          <div class="value" id="totalEarned">', '>累计总金额</div>\n          <div class="value" id="totalEarned">')
c = c.replace('id="totalEarned">?0.00</div>', 'id="totalEarned">¥0.00</div>')
c = c.replace('>???</div>\n          <div class="value" id="currentRound">', '>当前局</div>\n          <div class="value" id="currentRound">')
c = c.replace('>????</div>\n          <div class="value" id="remainingCount">', '>剩余红包</div>\n          <div class="value" id="remainingCount">')
c = c.replace('id="nextRoundBtn">?????</button>', 'id="nextRoundBtn">进入下一局</button>')
c = c.replace("document.getElementById('musicToggle').textContent = '? ??';", "document.getElementById('musicToggle').textContent = '开 音乐';", 1)
c = c.replace("document.getElementById('musicToggle').textContent = '? ??';", "document.getElementById('musicToggle').textContent = '关 音乐';", 1)
c = c.replace('<p class="subtitle">?????????</p>\n      </div>\n      <button', '<p class="subtitle">点击开始，好运连连</p>\n      </div>\n      <button', 1)
c = c.replace('<p class="subtitle">?????????</p>\n      </div>\n      \n      <div class="stats">', '<p class="subtitle">点击红包，好运连连</p>\n      </div>\n      \n      <div class="stats">', 1)
c = c.replace('<p style="margin-top:16px;color:rgba(255,255,255,0.6);font-size:14px">??????????</p>', '<p style="margin-top:16px;color:rgba(255,255,255,0.6);font-size:14px">点击下方按钮开始游戏</p>')
c = c.replace('<!-- ?? -->\n    <div id="startScreen"', '<!-- 开始 -->\n    <div id="startScreen"')
c = c.replace('<!-- ?? -->\n    <div id="gameArea"', '<!-- 游戏 -->\n    <div id="gameArea"')

with open(path, 'w', encoding='utf-8') as f:
    f.write(c)
with open(path, 'rb') as f: d = f.read()
if not d.startswith(b'\xef\xbb\xbf'):
    with open(path, 'wb') as f: f.write(b'\xef\xbb\xbf' + d)
print('OK')
