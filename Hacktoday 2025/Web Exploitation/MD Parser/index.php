<?php
class SimpleMarkdown {
    protected $codeSpans = [];

    public function parse(string $text): string {
        $text = str_replace(["\r\n", "\r"], "\n", $text);
        $lines = explode("\n", $text);
        $html = '';
        $i = 0;
        $n = count($lines);

        while ($i < $n) {
            $line = $lines[$i];
            if (preg_match('/^```(.*)$/', $line, $m)) {
                $lang = trim($m[1]);
                $i++;
                $codeLines = [];
                while ($i < $n && !preg_match('/^```\s*$/', $lines[$i])) {
                    $codeLines[] = $lines[$i];
                    $i++;
                }
                if ($i < $n && preg_match('/^```\s*$/', $lines[$i])) $i++;
                $code = implode("\n", $codeLines);
                $html .= '<pre><code' . ($lang ? ' class="language-'.htmlspecialchars($lang).'"' : '') . '>' . htmlspecialchars($code) . '</code></pre>\n';
                continue;
            }

            if (preg_match('/^\s*(\*\s*\*\s*\*|-{3,}|_{3,})\s*$/', $line)) {
                $html .= "<hr />\n";
                $i++;
                continue;
            }

            if (preg_match('/^(#{1,6})\s*(.*)$/', $line, $m)) {
                $level = strlen($m[1]);
                $content = $this->inlineParse(trim($m[2]));
                $html .= "<h{$level}>{$content}</h{$level}>\n";
                $i++;
                continue;
            }

            if (preg_match('/^>\s?(.*)$/', $line)) {
                $quoteLines = [];
                while ($i < $n && preg_match('/^>\s?(.*)$/', $lines[$i], $m)) {
                    $quoteLines[] = $m[1];
                    $i++;
                }
                $inner = $this->parse(implode("\n", $quoteLines)); // recursive parse
                $html .= "<blockquote>{$inner}</blockquote>\n";
                continue;
            }

            if (preg_match('/^\s*([\-*+])\s+(.*)$/', $line)) {
                $html .= "<ul>\n";
                while ($i < $n && preg_match('/^\s*([\-*+])\s+(.*)$/', $lines[$i], $m)) {
                    $html .= "  <li>" . $this->inlineParse($m[2]) . "</li>\n";
                    $i++;
                }
                $html .= "</ul>\n";
                continue;
            }

            if (preg_match('/^\s*\d+\.\s+(.*)$/', $line)) {
                $html .= "<ol>\n";
                while ($i < $n && preg_match('/^\s*\d+\.\s+(.*)$/', $lines[$i], $m)) {
                    $html .= "  <li>" . $this->inlineParse($m[1]) . "</li>\n";
                    $i++;
                }
                $html .= "</ol>\n";
                continue;
            }

            if (trim($line) === '') {
                $i++;
                continue;
            }

            $paraLines = [];
            while ($i < $n && trim($lines[$i]) !== '' &&
                !preg_match('/^(#{1,6})\s+/', $lines[$i]) &&
                !preg_match('/^```/', $lines[$i]) &&
                !preg_match('/^>\s?/', $lines[$i]) &&
                !preg_match('/^\s*([\-*+])\s+/', $lines[$i]) &&
                !preg_match('/^\s*\d+\.\s+/', $lines[$i]) &&
                !preg_match('/^\s*(\*\s*\*\s*\*|-{3,}|_{3,})\s*$/', $lines[$i])
            ) {
                $paraLines[] = $lines[$i];
                $i++;
            }
            $para = implode(' ', $paraLines);
            $html .= '<p>' . $this->inlineParse(trim($para)) . '</p>\n';
        }

        return $html;
    }

    protected function inlineParse(string $text): string {
        $this->codeSpans = [];
        $text = preg_replace_callback('/`([^`]+)`/', function($m) {
            $idx = count($this->codeSpans);
            $this->codeSpans[$idx] = '<code>' . htmlspecialchars($m[1]) . '</code>';
            return "\0CODE{$idx}\0";
        }, $text);

        $text = htmlspecialchars($text);
        $text = preg_replace_callback('/!\[([^\]]*)\]\(([^)]+)\)/', function($m) {
            $alt = htmlspecialchars($m[1]);
            $rawUrl = $m[2];
            $src = $this->imageSourceFromPath($rawUrl);
            return '<img src="' . $src . '" alt="' . $alt . '" />';
        }, $text);

        $text = preg_replace_callback('/\[([^\]]+)\]\(([^)]+)\)/', function($m) {
            $label = htmlspecialchars($m[1]);
            $url = $this->sanitizeUrl($m[2]);
            return '<a href="' . $url . '" target="_blank" rel="noopener noreferrer">' . $label . '</a>';
        }, $text);

        $text = preg_replace('/(\*\*|__)(.*?)\1/', '<strong>$2</strong>', $text);
        $text = preg_replace('/~~(.*?)~~/', '<del>$1</del>', $text);
        $text = preg_replace('/(\*|_)(.*?)\1/', '<em>$2</em>', $text);
        
        $text = preg_replace_callback('/\0CODE(\d+)\0/', function($m) {
            $idx = (int)$m[1];
            return $this->codeSpans[$idx] ?? '';
        }, $text);

        return $text;
    }

    protected function imageSourceFromPath(string $url): string {
        $url = trim($url);
        if (preg_match('/^<(.+)>$/', $url, $m)) $url = $m[1];
        if (preg_match('/^\s*(javascript):/i', $url)) return '#';
        if (preg_match('#^data:#i', $url)) return htmlspecialchars($url);

        $ctx = null;
        if (preg_match('#^https?://#i', $url)) {
            $ctx = stream_context_create([
                'http' => [ 'timeout' => 5, 'header' => "User-Agent: SimpleMarkdown/1.0\r\n", 'follow_location' => 1 ],
                'https' => [ 'timeout' => 5, 'header' => "User-Agent: SimpleMarkdown/1.0\r\n", 'follow_location' => 1 ],
            ]);
            if (!ini_get('allow_url_fopen')) return htmlspecialchars($url);
        }

        $data = @file_get_contents($url, false, $ctx);
        if ($data === false) return htmlspecialchars($url);
        if (function_exists('finfo_buffer')) {
            $finfo = finfo_open(FILEINFO_MIME_TYPE);
            $mime = finfo_buffer($finfo, $data);
            finfo_close($finfo);
        } else {
            $ext = strtolower(pathinfo(parse_url($url, PHP_URL_PATH) ?? '', PATHINFO_EXTENSION));
            $mime = $ext ? ('image/' . $ext) : 'application/octet-stream';
        }
        if (strpos($mime, 'image/') !== 0) {
            return htmlspecialchars($url);
        }

        return 'data:' . htmlspecialchars($mime) . ';base64,' . base64_encode($data);
    }

    protected function sanitizeUrl(string $url): string {
        $url = trim($url);
        if (preg_match('/^<(.+)>$/', $url, $m)) $url = $m[1];
        if (preg_match('/^\s*(javascript|data):/i', $url)) return '#';
        return htmlspecialchars($url);
    }
}

$inputMd = '';
if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['markdown'])) {
    $inputMd = $_POST['markdown'];
}

$parser = new SimpleMarkdown();
$rendered = $inputMd !== '' ? $parser->parse($inputMd) : '';

?>

<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>PHP Markdown Parser</title>
  <style>
    body { font-family: system-ui, -apple-system, "Segoe UI", Roboto, Helvetica, Arial; max-width: 960px; margin: 24px auto; padding: 0 16px; color: #111; }
    header { display:flex; align-items:center; gap:12px; margin-bottom:18px; }
    textarea { width:100%; min-height:260px; font-family: monospace; font-size:14px; padding:12px; box-sizing:border-box; border:1px solid #ddd; border-radius:8px; }
    .controls { display:flex; gap:12px; margin:8px 0 18px; }
    .preview { border:1px solid #eee; padding:18px; border-radius:8px; background:#fff; box-shadow:0 2px 8px rgba(0,0,0,0.03); }
    pre { background:#0f172a; color:#f8fafc; padding:12px; overflow:auto; border-radius:6px; }
    code { background:#f3f4f6; padding:2px 6px; border-radius:4px; }
    img { max-width:100%; height:auto; }
    form > .row { margin-bottom:12px; }
    .meta { color:#d00; font-size:13px }
    button { padding:8px 12px; border-radius:8px; border:1px solid #ddd; background:#fff; cursor:pointer }
  </style>
</head>
<body>
  <header>
    <h1>Markdown Parser</h1>
    <div class="meta"></div>
  </header>

  <form method="post" enctype="application/x-www-form-urlencoded">
    <div class="row">
      <label for="markdown">Paste Markdown below:</label>
      <textarea name="markdown" id="markdown" placeholder="# Hello\n\nWrite markdown here..."><?php echo htmlspecialchars($inputMd); ?></textarea>
    </div>
    <div class="controls">
      <button type="submit">Parse Markdown</button>
      <button type="button" onclick="document.getElementById('markdown').value='';">Clear</button>
    </div>
  </form>

  <section>
    <h2>Preview</h2>
    <div class="preview">
      <?php if ($rendered !== ''): ?>
        <?php echo $rendered; ?>
      <?php else: ?>
        <em>Parsed output will appear here after you submit Markdown.</em>
      <?php endif; ?>
    </div>
  </section>
</body>
</html>
