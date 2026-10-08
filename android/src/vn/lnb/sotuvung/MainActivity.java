package vn.lnb.sotuvung;

import android.app.Activity;
import android.os.Bundle;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.res.AssetFileDescriptor;
import android.graphics.Color;
import android.media.MediaPlayer;
import android.media.PlaybackParams;
import android.net.Uri;
import android.webkit.*;
import android.view.View;
import android.widget.Toast;
import android.widget.FrameLayout;
import org.json.JSONObject;
import java.io.*;
import java.nio.charset.StandardCharsets;

public final class MainActivity extends Activity {
    private WebView web;
    private FrameLayout container;
    private MediaPlayer player;
    private SharedPreferences prefs;
    private String exportData;
    private static final int EXPORT = 10, IMPORT = 11;

    @Override public void onCreate(Bundle state) {
        super.onCreate(state);
        prefs = getSharedPreferences("lingo", MODE_PRIVATE);
        getWindow().setStatusBarColor(Color.rgb(247,248,252));
        getWindow().setNavigationBarColor(Color.rgb(247,248,252));
        if (android.os.Build.VERSION.SDK_INT >= 35) getWindow().setDecorFitsSystemWindows(true);
        web = new WebView(this);
        container = new FrameLayout(this);
        container.setBackgroundColor(Color.rgb(247,248,252));
        container.addView(web, new FrameLayout.LayoutParams(FrameLayout.LayoutParams.MATCH_PARENT, FrameLayout.LayoutParams.MATCH_PARENT));
        web.setBackgroundColor(Color.rgb(247,248,252));
        web.getSettings().setJavaScriptEnabled(true);
        web.getSettings().setDomStorageEnabled(false);
        web.getSettings().setAllowFileAccess(true);
        web.getSettings().setAllowContentAccess(false);
        web.getSettings().setAllowFileAccessFromFileURLs(false);
        web.getSettings().setAllowUniversalAccessFromFileURLs(false);
        web.getSettings().setMediaPlaybackRequiresUserGesture(false);
        web.setWebChromeClient(new WebChromeClient());
        if (android.os.Build.VERSION.SDK_INT >= 35) {
            container.setOnApplyWindowInsetsListener((view, insets) -> {
                android.graphics.Insets bars = insets.getInsets(android.view.WindowInsets.Type.systemBars() | android.view.WindowInsets.Type.displayCutout());
                android.graphics.Insets keyboard = insets.getInsets(android.view.WindowInsets.Type.ime());
                view.setPadding(bars.left, bars.top, bars.right, Math.max(bars.bottom, keyboard.bottom));
                return android.view.WindowInsets.CONSUMED;
            });
        }
        web.addJavascriptInterface(new Bridge(), "Android");
        web.setWebViewClient(new WebViewClient() {
            @Override public boolean shouldOverrideUrlLoading(WebView view, WebResourceRequest request) {
                return true; // All UI and learning data are packaged assets. No external navigation.
            }
            @Override public void onPageFinished(WebView view, String url) {
                web.evaluateJavascript("window.nativeReady && window.nativeReady()", null);
            }
        });
        setContentView(container);
        web.loadUrl("file:///android_asset/www/index.html");
    }

    public final class Bridge {
        @JavascriptInterface public String load() { return prefs.getString("state", ""); }
        @JavascriptInterface public boolean save(String value) {
            try { new JSONObject(value); return prefs.edit().putString("state", value).commit(); }
            catch (Exception e) { return false; }
        }
        @JavascriptInterface public void theme(final boolean dark) {
            runOnUiThread(() -> {
                int color = dark ? Color.rgb(17,23,42) : Color.rgb(247,248,252);
                container.setBackgroundColor(color);
                web.setBackgroundColor(color);
                getWindow().setStatusBarColor(color);
                getWindow().setNavigationBarColor(color);
                getWindow().getDecorView().setSystemUiVisibility(dark ? 0 : View.SYSTEM_UI_FLAG_LIGHT_STATUS_BAR | View.SYSTEM_UI_FLAG_LIGHT_NAVIGATION_BAR);
            });
        }
        @JavascriptInterface public void play(final String id, final boolean slow) {
            if (!id.matches("[a-z0-9_-]+")) return;
            runOnUiThread(() -> {
                releaseAudio();
                try {
                    AssetFileDescriptor asset = getAssets().openFd("www/audio/"+id+".mp3");
                    player = new MediaPlayer();
                    player.setDataSource(asset.getFileDescriptor(), asset.getStartOffset(), asset.getLength());
                    asset.close();
                    player.setOnCompletionListener(mp -> releaseAudio());
                    player.prepare();
                    android.util.Log.i("LingoAudio", "Prepared " + id + ", duration=" + player.getDuration());
                    player.setPlaybackParams(new PlaybackParams().setSpeed(slow ? 0.78f : 1f));
                    player.start();
                } catch (Exception ex) {
                    android.util.Log.e("LingoAudio", "Playback failed", ex);
                    releaseAudio();
                    web.evaluateJavascript("window.audioFailed && window.audioFailed()", null);
                }
            });
        }
        @JavascriptInterface public void stop() { runOnUiThread(() -> releaseAudio()); }
        @JavascriptInterface public void exportBackup(String json) {
            exportData = json;
            runOnUiThread(() -> {
                Intent intent = new Intent(Intent.ACTION_CREATE_DOCUMENT);
                intent.setType("application/json");
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.putExtra(Intent.EXTRA_TITLE,"Lingo-backup.json");
                startActivityForResult(intent, EXPORT);
            });
        }
        @JavascriptInterface public void importBackup() {
            runOnUiThread(() -> {
                Intent intent = new Intent(Intent.ACTION_OPEN_DOCUMENT);
                intent.addCategory(Intent.CATEGORY_OPENABLE);
                intent.setType("*/*");
                startActivityForResult(intent, IMPORT);
            });
        }
    }
    @Override protected void onActivityResult(int request, int result, Intent data) {
        super.onActivityResult(request,result,data);
        if (result != RESULT_OK || data == null || data.getData() == null) return;
        try {
            if (request == EXPORT) {
                try (OutputStream out = getContentResolver().openOutputStream(data.getData())) {
                    out.write(exportData.getBytes(StandardCharsets.UTF_8));
                }
                Toast.makeText(this,"Đã lưu bản sao lưu",Toast.LENGTH_SHORT).show();
            } else if (request == IMPORT) {
                ByteArrayOutputStream out = new ByteArrayOutputStream();
                try (InputStream in = getContentResolver().openInputStream(data.getData())) {
                    byte[] buffer = new byte[4096]; int n;
                    while ((n=in.read(buffer)) != -1) {
                        out.write(buffer,0,n);
                        if (out.size() > 5*1024*1024) throw new IOException("Backup too large");
                    }
                }
                String json = out.toString("UTF-8");
                web.evaluateJavascript("window.receiveBackup("+JSONObject.quote(json)+")",null);
            }
        } catch (Exception ex) { Toast.makeText(this,"Không thể đọc/lưu bản sao lưu",Toast.LENGTH_LONG).show(); }
    }
    private void releaseAudio() {
        if (player != null) { player.release(); player = null; }
    }
    @Override protected void onPause() { releaseAudio(); super.onPause(); }
    @Override public void onBackPressed() {
        web.evaluateJavascript("window.handleBack()", value -> { if ("false".equals(value)) MainActivity.super.onBackPressed(); });
    }
    @Override protected void onDestroy() { releaseAudio(); web.destroy(); super.onDestroy(); }
}
