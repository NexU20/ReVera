import json
from pathlib import Path

notebook_path = Path("notebooks/00_laporan_akhir.ipynb")
with open(notebook_path, "r", encoding="utf-8") as f:
    nb = json.load(f)

md_cell = {
    "cell_type": "markdown",
    "metadata": {},
    "source": [
        "### 4.1 Word Cloud (Visualisasi Teks Bersih)\n",
        "\n",
        "Setelah teks dibersihkan (tahap *preprocessing* selesai), kita bisa memvisualisasikan kata-kata apa saja yang paling sering muncul di **Ulasan Negatif** dan **Ulasan Positif** menggunakan *Word Cloud*."
    ]
}

code_cell = {
    "cell_type": "code",
    "execution_count": None,
    "metadata": {},
    "outputs": [],
    "source": [
        "from wordcloud import WordCloud\n",
        "\n",
        "# Menggabungkan semua teks ulasan bersih berdasarkan sentimen\n",
        "neg_text = \" \".join(df[df[\"label_sentimen\"] == \"Negatif\"][\"ulasan_bersih\"].dropna())\n",
        "pos_text = \" \".join(df[df[\"label_sentimen\"] == \"Positif\"][\"ulasan_bersih\"].dropna())\n",
        "\n",
        "def plot_wordcloud(text, title, colormap):\n",
        "    # Jika tidak ada kata yang tersisa, kembalikan gambar kosong\n",
        "    if not text.strip():\n",
        "        print(f\"Tidak ada teks untuk {title}\")\n",
        "        return\n",
        "        \n",
        "    wc = WordCloud(width=800, height=400, background_color=\"white\", colormap=colormap, max_words=100)\n",
        "    wc.generate(text)\n",
        "    plt.figure(figsize=(10, 5))\n",
        "    plt.imshow(wc, interpolation=\"bilinear\")\n",
        "    plt.title(title, fontsize=16, fontweight=\"bold\")\n",
        "    plt.axis(\"off\")\n",
        "    plt.show()\n",
        "\n",
        "# Tampilkan Word Cloud Negatif\n",
        "plot_wordcloud(neg_text, \"Kata Terpopuler pada Ulasan Negatif\", \"Reds\")\n",
        "\n",
        "# Tampilkan Word Cloud Positif\n",
        "plot_wordcloud(pos_text, \"Kata Terpopuler pada Ulasan Positif\", \"Greens\")"
    ]
}

# Find the index of Cell 27 (Label Encoding) to insert after it
insert_idx = -1
for i, cell in enumerate(nb["cells"]):
    if cell["cell_type"] == "code" and cell["source"] and cell["source"][0].startswith("# Label Encoding"):
        insert_idx = i + 1
        break

if insert_idx != -1:
    nb["cells"].insert(insert_idx, md_cell)
    nb["cells"].insert(insert_idx + 1, code_cell)
    
    with open(notebook_path, "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=1, ensure_ascii=False)
    print("Word Cloud cells added successfully.")
else:
    print("Could not find insertion point.")
