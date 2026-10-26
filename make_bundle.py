"""仮置き場用の1ファイル版をつくる：three.js と 3D の2ページを、問題をえらぶページの中に入れる。
python make_bundle.py → 鏡の問題ラボ_中1理科_光による現象.html

3D のページは、カードを押したときに iframe（srcdoc）で開く。
three.js は親で動かさず、本文を文字として持っておき、開くときに 3D のページの中へ入れる
（親の THREE を借りると、ページをまたいだ instanceof が失敗して WebGL2 と判定されず、シェーダーがこわれる）。
"""
import base64, json, os
H = os.path.dirname(os.path.abspath(__file__))
rd = lambda f: open(os.path.join(H, f), encoding='utf-8').read()
b64 = lambda s: base64.b64encode(s.encode('utf-8')).decode('ascii')

def page3d(f):
    s = rd(f)
    s = s.replace('<script src="three.min.js"></script>', '<script>/*THREE*/</script>')
    s = s.replace('<a href="index.html">', '<a href="#" onclick="parent.__close3d();return false">')
    return b64(s)

tpl = {'kagami3d.html': page3d('kagami3d.html'), 'moji3d.html': page3d('moji3d.html')}
inject = """<script>
const __THREE=%s;
const __TPL=%s;
const __dec=b=>new TextDecoder().decode(Uint8Array.from(atob(b),c=>c.charCodeAt(0)));
window.__open3d=function(href){
  const f=href.split('?')[0];
  const html=__dec(__TPL[f]).replace('/*THREE*/',()=>__dec(__THREE));
  const fr=document.createElement('iframe'); fr.id='__fr3d';
  fr.style.cssText='position:fixed;inset:0;width:100vw;height:100vh;border:0;z-index:1000;background:#0f1216';
  fr.srcdoc=html; document.body.appendChild(fr); document.body.style.overflow='hidden';
};
window.__close3d=function(){ const f=document.getElementById('__fr3d'); if(f) f.remove(); document.body.style.overflow=''; };
</script>
""" % (json.dumps(b64(rd('three.min.js'))), json.dumps(tpl))

s = rd('index.html').replace('</body>', inject + '</body>')
out = os.path.join(H, '鏡の問題ラボ_中1理科_光による現象.html')
open(out, 'w', encoding='utf-8').write(s)
print('saved', os.path.basename(out), round(len(s.encode('utf-8')) / 1024), 'KB')
