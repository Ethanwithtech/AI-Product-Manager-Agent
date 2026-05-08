// ===== 场景切换 =====
function switchScene(id){
  document.querySelectorAll('.scene-container').forEach(function(s){s.classList.remove('active')});
  document.querySelectorAll('.scene-tab').forEach(function(t){t.classList.remove('active')});
  document.getElementById(id).classList.add('active');
  event.target.classList.add('active');
  // 切换后重绘连线
  setTimeout(drawAllLines, 200);
}

// ===== 聊天窗口开关 =====
function openChat(chatId){
  var el=document.getElementById(chatId);
  if(el){el.style.display='block';el.style.animation='fadeInUp .4s ease'}
}
function closeChat(chatId){
  var el=document.getElementById(chatId);
  if(el) el.style.display='none';
}

// ===== 发送消息 =====
function sendUserMsg(bodyId, text){
  var body=document.getElementById(bodyId);
  if(!body) return;
  var row=document.createElement('div');
  row.className='msg-row user';
  row.innerHTML='<div class="msg-avatar"><img src="demo-assets/avatar-user.jpg" alt="用户"></div><div class="msg-bubble">'+text+'</div>';
  body.appendChild(row);
  body.scrollTop=body.scrollHeight;
  setTimeout(function(){
    var bot=document.createElement('div');
    bot.className='msg-row bot';
    bot.innerHTML='<div class="msg-avatar"><img src="demo-assets/avatar-bot.jpg" alt="AI"></div><div class="msg-bubble"><div class="typing-dots"><span></span><span></span><span></span></div></div>';
    body.appendChild(bot);
    body.scrollTop=body.scrollHeight;
    setTimeout(function(){
      var responses={
        '满300减50活动':'当前店铺满300减50活动正在进行中，全场通用，可与会员折扣叠加使用！活动截止至本月底。',
        '双十一新品专区':'双十一新品专区已上线，精选20+新款，部分商品享首发价8折优惠！',
        '哪里发货？':'我们从广州仓库发货，支持顺丰、中通配送，一般1-3天送达。',
        '如何退款':'7天内无理由退换，请在「我的订单」中发起退款申请，审核通过后1-3个工作日原路退回。',
        '必抢爆款-仅7折':'本周爆款专区精选10件商品低至7折！其中包括热销积木套装和电动赛车，数量有限！',
        '超值满赠-满499正装豪礼':'满499元即赠正装豪礼一份（随机赠送限定版收藏盒或精美包装袋），活动截止本月底。',
        '支付打卡-最新款积木':'最新款城市系列积木已到货，原价299，打卡价259，支持分期免息！',
        '这款有没有现货':'您好！这款目前有现货，库存充足，下单后24小时内发货。',
        '怎么入驻你们平台':'欢迎入驻！入驻流程：提交企业资质 → 平台审核（3个工作日）→ 签署协议 → 开通店铺。',
        '我想做代理/分销':'感谢您的合作意向！分销政策包括区域保护、价格支持、培训支持等。',
        // ===== 平台客服场景 =====
        '平台退款规则':'📋 平台退款规则：<br><br>1️⃣ <b>7天无理由</b>：签收后7天内可发起无理由退货<br>2️⃣ <b>质量问题</b>：15天内可申请退换，运费商家承担<br>3️⃣ <b>极速退款</b>：信誉良好用户3小时极速到账<br>4️⃣ <b>仅退款</b>：商品破损/错发/漏发支持仅退款<br>5️⃣ <b>退款时效</b>：原路退回1-7个工作日到账<br><br>如商家拒绝履行退款，可发起<b>平台介入</b>申诉。',
        '举报商家':'🚨 举报商家通道已开启。<br><br>平台严厉打击以下违规行为：<br>• 虚假发货 / 虚构物流<br>• 假冒伪劣 / 描述不符<br>• 刷单炒信 / 虚假好评<br>• 辱骂客户 / 诱导交易<br>• 泄露用户信息<br><br>请提供 <b>订单号</b> 和 <b>问题描述</b>，平台将在24小时内核实处理，违规商家将面临扣分、下架、资金冻结等处罚。',
        '账号安全问题':'🔒 账号安全相关问题：<br><br>• <b>账号被盗</b>：立即冻结账号 → 身份核验 → 密码重置<br>• <b>登录异常</b>：触发二次验证，可使用手机号+人脸识别解锁<br>• <b>账号被冻结</b>：请提供实名信息和订单记录，人工审核后解除<br>• <b>实名认证</b>：需上传身份证正反面+手持照<br><br>涉及账户资金安全的问题将优先转人工处理。',
        '支付纠纷申诉':'⚖️ 支付纠纷处理流程：<br><br>1️⃣ 已扣款未下单 → 平台查询支付流水，2小时内原路退回<br>2️⃣ 重复扣款 → 系统自动识别，当天退回多扣款项<br>3️⃣ 商家未发货拒退款 → 平台强制介入，72小时内退款<br>4️⃣ 虚假交易扣款 → 转人工申诉+警方协助<br><br>请提供 <b>订单号 + 支付流水号</b>，我立即为您核查。',
        '平台活动规则':'🎁 当前平台活动规则：<br><br>1️⃣ <b>跨店满减</b>：满300减50，可跨店铺叠加<br>2️⃣ <b>平台券</b>：每天10点发放，单笔最高抵100<br>3️⃣ <b>保价服务</b>：15天内降价自动退差价<br>4️⃣ <b>先用后付</b>：0元下单，确认收货后付款<br>5️⃣ <b>PLUS会员</b>：额外95折 + 运费券<br><br>📖 查看 <a style="color:#1a73e8;text-decoration:underline">完整活动规则</a>',
        '发票相关问题':'🧾 发票开具说明：<br><br>• <b>电子普通发票</b>：下单时勾选，签收后3天内自动开具<br>• <b>增值税专用发票</b>：需提前提交公司资质（营业执照、税务登记证）<br>• <b>补开发票</b>：签收后180天内可补开<br>• <b>发票换开</b>：如需修改抬头/税号，联系商家作废重开<br><br>发票问题如商家未处理，可申请 <b>平台协助</b>开具。'
      };
      var resp=responses[text]||'感谢您的咨询！关于"'+text+'"，我来为您详细解答。请稍候...';
      bot.querySelector('.msg-bubble').innerHTML=resp;
      body.scrollTop=body.scrollHeight;
    },1200);
  },400);
}

function sendFromInput(bodyId, inputId){
  var input=document.getElementById(inputId);
  if(!input||!input.value.trim())return;
  sendUserMsg(bodyId, input.value.trim());
  input.value='';
}

// ===== 询盘流程动画 =====
var iqPlayed=false;
function playInquiry(){
  if(iqPlayed) return; iqPlayed=true;
  var steps=['iq-step1','iq-step2','iq-step3','iq-step4','iq-step5','iq-step6'];
  var delays=[500,1400,1000,1400,1000,1800]; var total=0;
  steps.forEach(function(id,i){total+=delays[i];setTimeout(function(){var el=document.getElementById(id);if(el){el.style.display='flex';document.getElementById('chatBody2').scrollTop=99999}},total)});
}

// ===== 物流查询动画 =====
var logPlayed=false;
function showLogistics(){
  if(logPlayed) return; logPlayed=true;
  document.getElementById('order-q').style.display='flex';
  setTimeout(function(){document.getElementById('order-a').style.display='flex';
    setTimeout(function(){document.getElementById('order-b').style.display='flex'},1200);
  },600);
}

// ===== 多入口场景切换 =====
function switchEntry(entry){
  document.querySelectorAll('.entry-tab').forEach(function(t){t.classList.remove('active')});
  event.target.classList.add('active');
  // 切换左侧来源页
  document.querySelectorAll('.entry-source').forEach(function(c){c.style.display='none'});
  var src = document.getElementById('src-'+entry);
  if(src) src.style.display='block';
  // 切换右侧聊天
  document.querySelectorAll('.entry-chat').forEach(function(c){c.style.display='none'});
  var chat = document.getElementById('entry-'+entry);
  if(chat) chat.style.display='block';
  // 重绘连线
  setTimeout(drawAllLines, 100);
}

// ===== 通用连线绘制函数 =====
function drawLine(svgId, leftEl, rightEl, color, labelText){
  var svg = document.getElementById(svgId);
  if(!svg || !leftEl || !rightEl) return;
  var layout = svg.parentElement;
  var lr = layout.getBoundingClientRect();
  var leftR = leftEl.getBoundingClientRect();
  var rightR = rightEl.getBoundingClientRect();

  // 起点：左侧元素的右边中点
  var x1 = leftR.right - lr.left;
  var y1 = leftR.top + leftR.height/2 - lr.top;
  // 终点：右侧元素的左边中点
  var x2 = rightR.left - lr.left;
  var y2 = rightR.top + rightR.height/2 - lr.top;

  svg.setAttribute('viewBox', '0 0 '+Math.round(lr.width)+' '+Math.round(lr.height));
  svg.style.width = lr.width+'px';
  svg.style.height = lr.height+'px';

  var cpx1 = x1 + (x2-x1)*0.4;
  var cpx2 = x1 + (x2-x1)*0.6;
  var path = 'M'+x1+','+y1+' C'+cpx1+','+y1+' '+cpx2+','+y2+' '+x2+','+y2;

  var labelX = (x1+x2)/2;
  var labelY = (y1+y2)/2 - 14;

  svg.innerHTML = '<path d="'+path+'" stroke="'+color+'" stroke-width="2.5" stroke-dasharray="8,5" fill="none"/>'
    + '<circle cx="'+x1+'" cy="'+y1+'" r="5" fill="'+color+'"/>'
    + '<circle cx="'+x2+'" cy="'+y2+'" r="5" fill="'+color+'"/>'
    + '<rect x="'+(labelX-36)+'" y="'+(labelY-10)+'" width="72" height="20" rx="10" fill="'+color+'"/>'
    + '<text x="'+labelX+'" y="'+(labelY+3)+'" text-anchor="middle" fill="#fff" font-size="10" font-weight="600">'+labelText+'</text>';
}

function drawAllLines(){
  // 场景一：2条线
  var pc1 = document.getElementById('pc1');
  var pc2 = document.getElementById('pc2');
  var chatA = document.getElementById('chat1a');
  var chatB = document.getElementById('chat1b');
  var svg1 = document.getElementById('s1-lines');
  if(svg1 && pc1 && pc2 && chatA && chatB){
    var layout = svg1.parentElement;
    var lr = layout.getBoundingClientRect();
    var r1=pc1.getBoundingClientRect(), r2=pc2.getBoundingClientRect();
    var rA=chatA.getBoundingClientRect(), rB=chatB.getBoundingClientRect();

    var x1a=r1.right-lr.left, y1a=r1.top+r1.height/2-lr.top;
    var x2a=rA.left-lr.left, y2a=rA.top+rA.height/2-lr.top;
    var x1b=r2.right-lr.left, y1b=r2.top+r2.height/2-lr.top;
    var x2b=rB.left-lr.left, y2b=rB.top+rB.height/2-lr.top;

    svg1.setAttribute('viewBox','0 0 '+Math.round(lr.width)+' '+Math.round(lr.height));
    svg1.style.width=lr.width+'px'; svg1.style.height=lr.height+'px';

    var cpA1=x1a+(x2a-x1a)*.4, cpA2=x1a+(x2a-x1a)*.6;
    var cpB1=x1b+(x2b-x1b)*.4, cpB2=x1b+(x2b-x1b)*.6;
    var pathA='M'+x1a+','+y1a+' C'+cpA1+','+y1a+' '+cpA2+','+y2a+' '+x2a+','+y2a;
    var pathB='M'+x1b+','+y1b+' C'+cpB1+','+y1b+' '+cpB2+','+y2b+' '+x2b+','+y2b;
    var lxA=(x1a+x2a)/2, lyA=(y1a+y2a)/2-14;
    var lxB=(x1b+x2b)/2, lyB=(y1b+y2b)/2-14;

    svg1.innerHTML =
      '<path d="'+pathA+'" stroke="#e4393c" stroke-width="2.5" stroke-dasharray="8,5" fill="none"/>'
      +'<circle cx="'+x1a+'" cy="'+y1a+'" r="5" fill="#e4393c"/><circle cx="'+x2a+'" cy="'+y2a+'" r="5" fill="#e4393c"/>'
      +'<rect x="'+(lxA-36)+'" y="'+(lyA-10)+'" width="72" height="20" rx="10" fill="#e4393c"/>'
      +'<text x="'+lxA+'" y="'+(lyA+3)+'" text-anchor="middle" fill="#fff" font-size="10" font-weight="600">客服号 A</text>'
      +'<path d="'+pathB+'" stroke="#1a73e8" stroke-width="2.5" stroke-dasharray="8,5" fill="none"/>'
      +'<circle cx="'+x1b+'" cy="'+y1b+'" r="5" fill="#1a73e8"/><circle cx="'+x2b+'" cy="'+y2b+'" r="5" fill="#1a73e8"/>'
      +'<rect x="'+(lxB-36)+'" y="'+(lyB-10)+'" width="72" height="20" rx="10" fill="#1a73e8"/>'
      +'<text x="'+lxB+'" y="'+(lyB+3)+'" text-anchor="middle" fill="#fff" font-size="10" font-weight="600">客服号 B</text>';
  }

  // 场景三：来源页 → 聊天
  var s3svg = document.getElementById('s3-lines');
  var s3src = document.getElementById('entry-source-phone');
  var s3chat = document.getElementById('s3-chat');
  if(s3svg && s3src && s3chat){
    drawLine('s3-lines', s3src, s3chat, '#e4393c', '进入客服');
  }

  // 场景四：订单页 → 聊天
  var s4svg = document.getElementById('s4-lines');
  var s4src = document.getElementById('order-card-1');
  var s4phones = document.querySelectorAll('#s4 .chat-phone');
  if(s4svg && s4src && s4phones.length>0){
    drawLine('s4-lines', s4src, s4phones[0], '#1a73e8', '联系客服');
  }

  // 场景十五：平台服务中心 → 平台客服
  var s15svg = document.getElementById('s15-lines');
  var s15src = document.getElementById('platform-service-card');
  var s15chat = document.getElementById('s15-chat');
  if(s15svg && s15src && s15chat){
    drawLine('s15-lines', s15src, s15chat, '#1a73e8', '平台客服');
  }
}

// ===== 初始化 =====
setTimeout(function(){
  openChat('chat1a');
  openChat('chat1b');
  setTimeout(drawAllLines, 300);
},600);

window.addEventListener('resize', function(){ setTimeout(drawAllLines, 200); });

// ===== 全局头像/图片注入 =====
document.addEventListener('DOMContentLoaded', function(){
  var avatarMap = {
    'AI':'demo-assets/avatar-bot.jpg','我':'demo-assets/avatar-user.jpg',
    'Me':'demo-assets/avatar-user.jpg','私':'demo-assets/avatar-user.jpg',
    '买':'demo-assets/avatar-user2.jpg','客':'demo-assets/avatar-cs1.jpg',
    '美':'demo-assets/avatar-cs2.jpg','营':'demo-assets/avatar-bot.jpg',
    'V':'demo-assets/avatar-vip.jpg','张':'demo-assets/avatar-vip.jpg',
    '物':'demo-assets/avatar-logistics.jpg'
  };
  document.querySelectorAll('.msg-avatar').forEach(function(el){
    if(el.querySelector('img')) return;
    var text=el.textContent.trim();
    var src=avatarMap[text];
    if(src) el.innerHTML='<img src="'+src+'" alt="'+text+'">';
  });
  document.querySelectorAll('.pm-img').forEach(function(el){
    if(el.querySelector('img')) return;
    el.innerHTML='<img src="demo-assets/toy2.jpg" alt="商品">';
    el.style.background='#f5f5f5';
  });
  document.querySelectorAll('.o-img').forEach(function(el){
    if(el.querySelector('img')) return;
    el.innerHTML='<img src="demo-assets/figurine1.jpg" alt="商品" style="width:100%;height:100%;object-fit:cover;border-radius:4px">';
    el.style.background='#f5f5f5';
  });
});
