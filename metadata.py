from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TPOS, TPE2

file = "1-1. 新出単語（しんしゅつたんご）⑤.mp3"
title = "新出単語（しんしゅつたんご）⑤"
artist = "<名> 新单词；生词"
album = "综合日语第一册单词2-1"
track_num = 1
disc_num = 1
album_artist = "综合日语"


def set_mp3_metadata(
    file_path, title, artist, album, track_num, disc_num, album_artist
):
    try:
        try:
            audio = MP3(file_path, ID3=ID3)
        except:
            audio = MP3(file_path)

        if audio.tags is None:
            audio.add_tags()

        if title:
            audio.tags.add(TIT2(encoding=3, text=title))  # 歌曲标题
        if artist:
            audio.tags.add(TPE1(encoding=3, text=artist))  # 歌手/艺术家
        if album:
            audio.tags.add(TALB(encoding=3, text=album))  # 专辑名称
        if track_num:
            audio.tags.add(TRCK(encoding=3, text=str(track_num)))  # 音轨号
        if disc_num:
            audio.tags.add(TPOS(encoding=3, text=str(disc_num)))  # Disc号
        if album_artist:
            audio.tags.add(TPE2(encoding=3, text=album_artist))  # 专辑艺术家

        audio.save()
        print(f"成功更新文件 '{file_path}' 的元数据")
        return False
    except Exception as e:
        print(f"处理文件 '{file_path}' 时出错: {str(e)}")
        return True


if __name__ == "__main__":
    set_mp3_metadata(file, title, artist, album, track_num, disc_num, album_artist)
