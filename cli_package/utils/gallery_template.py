import os

def build_gallery_html(chat_title, data):
    """
    Generates a highly-stylized, responsive HTML gallery based on the downloaded media.
    Separated from utils/download.py to keep the main logic clean.
    """
    # Sort data by message_id descending (newest first)
    sorted_data = sorted(data, key=lambda x: x.get("message_id", 0), reverse=True)
    
    # Calculate stats
    total_files = len(sorted_data)
    photos_count = sum(1 for x in sorted_data if x.get("media_type") == "photo")
    videos_count = sum(1 for x in sorted_data if x.get("media_type") == "video")
    audios_count = sum(1 for x in sorted_data if x.get("media_type") in ("audio", "voice"))
    docs_count = sum(1 for x in sorted_data if x.get("media_type") not in ("photo", "video", "audio", "voice"))
    
    # Collect unique topic names if any exist
    topics = sorted(list(set(x.get("topic_name") for x in sorted_data if x.get("topic_name"))))
    
    html_content = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{chat_title} - Media Gallery</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&display=swap" rel="stylesheet">
    <style>
        :root {{
            --bg-color: #0b0f19;
            --card-bg: rgba(255, 255, 255, 0.03);
            --card-border: rgba(255, 255, 255, 0.08);
            --primary-color: #0088cc; /* Telegram blue */
            --primary-glow: rgba(0, 136, 204, 0.4);
            --text-color: #f3f4f6;
            --text-muted: #9ca3af;
        }}
        
        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}
        
        body {{
            font-family: 'Outfit', sans-serif;
            background: linear-gradient(135deg, #0b0f19 0%, #111827 100%);
            color: var(--text-color);
            min-height: 100vh;
            padding: 2rem;
        }}
        
        .header {{
            max-width: 1400px;
            margin: 0 auto 2rem auto;
            text-align: center;
            background: rgba(255, 255, 255, 0.02);
            backdrop-filter: blur(10px);
            border: 1px solid var(--card-border);
            border-radius: 20px;
            padding: 2rem;
        }}
        
        .header h1 {{
            font-size: 2.5rem;
            font-weight: 800;
            background: linear-gradient(to right, #0088cc, #00c6ff);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }}
        
        .header p {{
            color: var(--text-muted);
            font-size: 1.1rem;
        }}
        
        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(150px, 1fr));
            gap: 1rem;
            max-width: 1400px;
            margin: 0 auto 2rem auto;
        }}
        
        .stat-card {{
            background: rgba(255, 255, 255, 0.02);
            border: 1px solid var(--card-border);
            border-radius: 15px;
            padding: 1rem;
            text-align: center;
            backdrop-filter: blur(5px);
            transition: transform 0.3s ease;
        }}
        
        .stat-card:hover {{
            transform: translateY(-5px);
            border-color: var(--primary-color);
        }}
        
        .stat-num {{
            font-size: 1.8rem;
            font-weight: 800;
            color: var(--primary-color);
        }}
        
        .stat-label {{
            font-size: 0.9rem;
            color: var(--text-muted);
            margin-top: 0.2rem;
            text-transform: uppercase;
            letter-spacing: 1px;
        }}
        
        .controls {{
            max-width: 1400px;
            margin: 0 auto 2rem auto;
            display: flex;
            flex-wrap: wrap;
            gap: 1rem;
            justify-content: space-between;
            align-items: center;
        }}
        
        .search-bar {{
            flex: 1;
            min-width: 300px;
            position: relative;
        }}
        
        .search-bar input {{
            width: 100%;
            padding: 0.8rem 1.5rem;
            background: rgba(255, 255, 255, 0.04);
            border: 1px solid var(--card-border);
            border-radius: 30px;
            color: var(--text-color);
            font-family: inherit;
            font-size: 1rem;
            outline: none;
            transition: all 0.3s ease;
        }}
        
        .search-bar input:focus {{
            border-color: var(--primary-color);
            box-shadow: 0 0 15px var(--primary-glow);
            background: rgba(255, 255, 255, 0.07);
        }}
        
        .filter-buttons {{
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
        }}
        
        .filter-btn {{
            padding: 0.6rem 1.2rem;
            border: 1px solid var(--card-border);
            border-radius: 20px;
            background: rgba(255, 255, 255, 0.02);
            color: var(--text-color);
            cursor: pointer;
            font-family: inherit;
            font-size: 0.9rem;
            transition: all 0.3s ease;
        }}
        
        .filter-btn:hover, .filter-btn.active {{
            background: var(--primary-color);
            border-color: var(--primary-color);
            box-shadow: 0 0 10px var(--primary-glow);
        }}
        
        .gallery-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
            gap: 2rem;
            max-width: 1400px;
            margin: 0 auto;
        }}
        
        .media-card {{
            background: var(--card-bg);
            border: 1px solid var(--card-border);
            border-radius: 18px;
            overflow: hidden;
            display: flex;
            flex-direction: column;
            backdrop-filter: blur(10px);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        }}
        
        .media-card:hover {{
            transform: translateY(-10px);
            border-color: var(--primary-color);
            box-shadow: 0 10px 30px rgba(0, 136, 204, 0.15);
        }}
        
        .media-preview {{
            position: relative;
            aspect-ratio: 16/9;
            background: #000;
            overflow: hidden;
            display: flex;
            align-items: center;
            justify-content: center;
        }}
        
        .media-preview img, .media-preview video {{
            width: 100%;
            height: 100%;
            object-fit: cover;
            transition: transform 0.5s ease;
        }}
        
        .media-card:hover .media-preview img {{
            transform: scale(1.05);
        }}
        
        .media-preview audio {{
            width: 90%;
        }}
        
        .document-preview {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            gap: 0.5rem;
            color: var(--text-muted);
            width: 100%;
            height: 100%;
            background: linear-gradient(135deg, #1f2937 0%, #111827 100%);
        }}
        
        .document-icon {{
            font-size: 3rem;
        }}
        
        .media-info {{
            padding: 1.2rem;
            display: flex;
            flex-direction: column;
            flex-grow: 1;
            justify-content: space-between;
            gap: 0.8rem;
        }}
        
        .media-meta {{
            display: flex;
            justify-content: space-between;
            font-size: 0.8rem;
            color: var(--text-muted);
        }}
        
        .media-caption {{
            font-size: 0.95rem;
            line-height: 1.4;
            color: var(--text-color);
            display: -webkit-box;
            -webkit-line-clamp: 3;
            -webkit-box-orient: vertical;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        
        .media-filename {{
            font-size: 0.8rem;
            color: var(--text-muted);
            word-break: break-all;
            background: rgba(0, 0, 0, 0.2);
            padding: 0.3rem 0.6rem;
            border-radius: 6px;
        }}
        
        .media-actions {{
            display: flex;
            gap: 0.5rem;
            margin-top: auto;
        }}
        
        .btn {{
            flex: 1;
            padding: 0.6rem;
            border-radius: 8px;
            font-family: inherit;
            font-size: 0.85rem;
            font-weight: 600;
            text-align: center;
            text-decoration: none;
            cursor: pointer;
            transition: all 0.2s ease;
        }}
        
        .btn-primary {{
            background: var(--primary-color);
            color: #fff;
            border: none;
        }}
        
        .btn-primary:hover {{
            background: #00a2f3;
            box-shadow: 0 0 10px var(--primary-glow);
        }}
        
        /* Lightbox modal styles */
        .lightbox {{
            display: none;
            position: fixed;
            z-index: 9999;
            top: 0;
            left: 0;
            width: 100%;
            height: 100%;
            background: rgba(0, 0, 0, 0.9);
            align-items: center;
            justify-content: center;
            padding: 2rem;
        }}
        
        .lightbox-content {{
            max-width: 90%;
            max-height: 90%;
        }}
        
        .lightbox-content img {{
            width: 100%;
            height: 100%;
            object-fit: contain;
            border-radius: 10px;
        }}
        
        .lightbox-close {{
            position: absolute;
            top: 2rem;
            right: 2rem;
            color: #fff;
            font-size: 3rem;
            cursor: pointer;
            transition: color 0.2s ease;
        }}
        
        .lightbox-close:hover {{
            color: var(--primary-color);
        }}
    </style>
</head>
<body>

    <div class="header">
        <h1>{chat_title}</h1>
        <p>Telegram Media Archive Gallery</p>
    </div>
    
    <div class="stats-grid">
        <div class="stat-card">
            <div class="stat-num">{total_files}</div>
            <div class="stat-label">Total Files</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{photos_count}</div>
            <div class="stat-label">📷 Photos</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{videos_count}</div>
            <div class="stat-label">🎥 Videos</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{audios_count}</div>
            <div class="stat-label">🎵 Audios</div>
        </div>
        <div class="stat-card">
            <div class="stat-num">{docs_count}</div>
            <div class="stat-label">📄 Documents</div>
        </div>
    </div>
    
    <div class="controls">
        <div class="search-bar">
            <input type="text" id="search" placeholder="Search by caption, filename, date..." onkeyup="filterGallery()">
        </div>
        
        {"".join(f'''
        <div class="filter-topic" id="topic-filter-container">
            <select id="topic-select" onchange="filterGallery()" style="padding: 0.6rem 1.2rem; border: 1px solid var(--card-border); border-radius: 20px; background: rgba(255, 255, 255, 0.02); color: var(--text-color); font-family: inherit; font-size: 0.9rem; outline: none; transition: all 0.3s ease;">
                <option value="all">All Topics</option>
                {"".join(f'<option value="{t}">{t}</option>' for t in topics)}
            </select>
        </div>
        ''' if topics else "")}
        
        <div class="filter-buttons">
            <button class="filter-btn active" onclick="setFilter('all', this)">All</button>
            <button class="filter-btn" onclick="setFilter('photo', this)">Photos</button>
            <button class="filter-btn" onclick="setFilter('video', this)">Videos</button>
            <button class="filter-btn" onclick="setFilter('audio', this)">Audios</button>
            <button class="filter-btn" onclick="setFilter('document', this)">Documents</button>
        </div>
    </div>
    
    <div class="gallery-grid" id="gallery">
"""
    
    # Populate items
    for item in sorted_data:
        mtype = item.get("media_type", "document")
        filename = item.get("filename", "")
        local_path = filename
        
        date_str = item.get("date", "")
        caption = item.get("caption", "")
        file_size = item.get("file_size", 0)
        file_size_mb = f"{file_size / (1024 * 1024):.2f} MB" if file_size > 0 else "Unknown"
        message_id = item.get("message_id", 0)
        topic_name = item.get("topic_name", "")
        
        # Preview rendering
        preview_html = ""
        action_btn_html = f'<a href="{local_path}" target="_blank" class="btn btn-primary">Open File</a>'
        
        if mtype == "photo":
            preview_html = f'<img src="{local_path}" alt="{filename}" onclick="openLightbox(this.src)" style="cursor: pointer;">'
        elif mtype == "video":
            preview_html = f'<video src="{local_path}" controls preload="metadata"></video>'
        elif mtype in ("audio", "voice"):
            preview_html = f'<div class="document-preview"><span class="document-icon">🎵</span><audio src="{local_path}" controls></audio></div>'
        else:
            doc_icon = "📄"
            if filename.lower().endswith((".zip", ".rar", ".7z", ".tar", ".gz")):
                doc_icon = "📦"
            elif filename.lower().endswith((".pdf", ".epub")):
                doc_icon = "📕"
            elif filename.lower().endswith((".doc", ".docx", ".txt", ".odt")):
                doc_icon = "📝"
            
            preview_html = f"""<div class="document-preview">
                <span class="document-icon">{doc_icon}</span>
                <span style="font-size: 0.9rem; text-align: center; padding: 0 1rem; color: var(--text-muted);">{filename[:40]}</span>
            </div>"""

        # Format caption to escape HTML tags
        safe_caption = caption.replace("<", "&lt;").replace(">", "&gt;").replace("\n", "<br>")
        
        html_content += f"""
        <div class="media-card" data-type="{mtype}" data-filename="{filename.lower()}" data-caption="{caption.lower()}" data-date="{date_str}" data-topic="{topic_name}">
            <div class="media-preview">
                {preview_html}
            </div>
            <div class="media-info">
                <div class="media-meta">
                    <span>📅 {date_str}</span>
                    <span>💾 {file_size_mb}</span>
                </div>
                {f'<div class="media-topic" style="font-size: 0.85rem; color: var(--primary-color); font-weight: 600; margin-top: 0.2rem;">🏷️ {topic_name}</div>' if topic_name else ''}
                {f'<div class="media-caption">{safe_caption}</div>' if caption else ''}
                <div class="media-filename">{filename}</div>
                <div class="media-actions">
                    {action_btn_html}
                    <a href="https://t.me/c/{chat_title.replace(" ", "_")}/{message_id}" target="_blank" class="btn" style="border: 1px solid var(--card-border); color: var(--text-muted);">View in TG</a>
                </div>
            </div>
        </div>
"""

    html_content += """
    </div>
    
    <div class="lightbox" id="lightbox" onclick="closeLightbox()">
        <span class="lightbox-close">&times;</span>
        <img class="lightbox-content" id="lightbox-img" src="">
    </div>
    
    <script>
        let currentFilter = 'all';
        
        function setFilter(type, btn) {
            currentFilter = type;
            document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
            filterGallery();
        }
        
        function filterGallery() {
            const query = document.getElementById('search').value.toLowerCase();
            const topicSelect = document.getElementById('topic-select');
            const selectedTopic = topicSelect ? topicSelect.value : 'all';
            const cards = document.querySelectorAll('.media-card');
            
            cards.forEach(card => {
                const type = card.getAttribute('data-type');
                const filename = card.getAttribute('data-filename');
                const caption = card.getAttribute('data-caption');
                const date = card.getAttribute('data-date');
                const topic = card.getAttribute('data-topic');
                
                const matchesSearch = filename.includes(query) || caption.includes(query) || date.includes(query);
                
                let matchesFilter = false;
                if (currentFilter === 'all') {
                    matchesFilter = true;
                } else if (currentFilter === 'audio') {
                    matchesFilter = (type === 'audio' || type === 'voice');
                } else if (currentFilter === 'document') {
                    matchesFilter = (type !== 'photo' && type !== 'video' && type !== 'audio' && type !== 'voice');
                } else {
                    matchesFilter = (type === currentFilter);
                }
                
                let matchesTopic = true;
                if (selectedTopic !== 'all') {
                    matchesTopic = (topic === selectedTopic);
                }
                
                if (matchesSearch && matchesFilter && matchesTopic) {
                    card.style.display = 'flex';
                } else {
                    card.style.display = 'none';
                }
            });
        }
        
        function openLightbox(src) {
            document.getElementById('lightbox-img').src = src;
            document.getElementById('lightbox').style.display = 'flex';
        }
        
        function closeLightbox() {
            document.getElementById('lightbox').style.display = 'none';
        }
    </script>
</body>
</html>
"""
    return html_content
