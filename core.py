import os
import zipfile
import tempfile
import shutil
import sqlite3

# ---------- XML ----------
def create_xml(series, number, title, author, tags, summary, number_float=None):
    extra = f"<NumberFloat>{number_float}</NumberFloat>" if number_float else ""

    return f'''<?xml version="1.0" encoding="utf-8"?>
<ComicInfo>
  <Title>{title}</Title>
  <Series>{series}</Series>
  <Number>{number}</Number>
  {extra}

  <Writer>{author}</Writer>
  <Tags>{tags}</Tags>
  <Summary>{summary}</Summary>
</ComicInfo>
'''


# ---------- ZIP ----------
def process_cbz(file_path, series, number, title, author, tags, summary, number_float=None):
    temp_fd, temp_path = tempfile.mkstemp(suffix=".cbz")
    os.close(temp_fd)

    with zipfile.ZipFile(file_path, 'r') as zin:
        with zipfile.ZipFile(temp_path, 'w') as zout:
            for item in zin.infolist():
                if item.filename.lower() != "comicinfo.xml":
                    zout.writestr(item, zin.read(item.filename))

            zout.writestr("ComicInfo.xml", create_xml(
                series, number, title, author, tags, summary, number_float
            ))

    shutil.move(temp_path, file_path)


# ---------- NUMBER ----------
def extract_numbers(folder_name):
    try:
        return int(folder_name), None
    except:
        try:
            val = float(folder_name)
            return int(val), val
        except:
            return None, None


# ---------- CALIBRE DB (CORRECT MATCHING) ----------

def get_metadata_from_db(db_path, title):
    conn = sqlite3.connect(f"file:{db_path}?mode=ro", uri=True)
    cur = conn.cursor()

    print("DB search (title):", title)

    cur.execute("""
        SELECT id FROM books
        WHERE title LIKE ?
    """, (f"%{title}%",))

    book = cur.fetchone()

    print("DB result:", book)

    if not book:
        conn.close()
        return None

    book_id = book[0]

    # author
    cur.execute("""
        SELECT name FROM authors
        JOIN books_authors_link ON authors.id = books_authors_link.author
        WHERE books_authors_link.book = ?
    """, (book_id,))
    author = ", ".join([a[0] for a in cur.fetchall()])

    # tags
    cur.execute("""
        SELECT name FROM tags
        JOIN books_tags_link ON tags.id = books_tags_link.tag
        WHERE books_tags_link.book = ?
    """, (book_id,))
    tags = ", ".join([t[0] for t in cur.fetchall()])

    # series
    cur.execute("""
        SELECT series.name FROM series
        JOIN books_series_link ON series.id = books_series_link.series
        WHERE books_series_link.book = ?
    """, (book_id,))
    row = cur.fetchone()
    series = row[0] if row else ""

    conn.close()

    return {
        "author": author,
        "tags": tags,
        "series": series
    }



def debug_db(db_path):
    import sqlite3

    conn = sqlite3.connect(db_path)
    cur = conn.cursor()

    print("\n--- BOOK COUNT ---")
    cur.execute("SELECT COUNT(*) FROM books")
    print(cur.fetchone())

    conn.close()


# ---------- MAIN ----------
def process_folder(folder, db_path, default_series, default_author, default_tags, summary):
    if not os.path.isdir(folder):
        raise Exception("Invalid folder")

    use_db = bool(db_path and os.path.isfile(db_path))

    if use_db:
        debug_db(db_path)

    cbz_files = []

    for root, _, files in os.walk(folder):
        for f in files:
            if f.lower().endswith(".cbz"):
                cbz_files.append(os.path.join(root, f))

    cbz_files.sort()

    processed = 0

    for full_path in cbz_files:
        filename = os.path.basename(full_path)
        title = os.path.splitext(filename)[0]

        parent = os.path.basename(os.path.dirname(full_path))
        number, number_float = extract_numbers(parent)

        if number is None:
            print(f"Skipping: {full_path}")
            continue

        # ---------- DB OR MANUAL ----------
        if use_db:
            series_name = os.path.basename(os.path.dirname(os.path.dirname(full_path)))

            print("Series detected:", series_name)
            print("Number:", number)

            meta = get_metadata_from_db(db_path, title)
        else:
            meta = None

        if meta:
            author = meta["author"] or default_author
            tags = meta["tags"] or default_tags
            series = meta["series"] or default_series
        else:
            author = default_author
            tags = default_tags
            series = default_series

        process_cbz(full_path, series, number, title, author, tags, summary, number_float)

        print(f"[{number}] {title}")
        processed += 1

    return processed