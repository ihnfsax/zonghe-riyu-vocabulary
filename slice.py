from pydub import AudioSegment
from pydub.silence import split_on_silence
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, TIT2, TPE1, TALB, TRCK, TPOS, TPE2
import csv
import shutil

audio_path = "2-1.mp3"
audio_type = "mp3"
file1 = "2-1 新出単語.csv"
file2 = "2-1 練習用単語.csv"
unit = "综合日语第一册2-1"
book = "综合日语"


def split_audio():
    audio = AudioSegment.from_file(audio_path, format=audio_type)
    print("分割音频中...")
    chunks = split_on_silence(
        audio, min_silence_len=550, silence_thresh=-45, keep_silence=100
    )
    print("保存音频片段中...")
    for i in range(len(chunks)):
        new = chunks[i]
        save_name = "chunks{}.{}".format(i + 1, audio_type)
        new.export(save_name, format=audio_type)
    return len(chunks)


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


def copy_file(old_name, new_name):
    try:
        shutil.copy2(old_name, new_name)
        print(f"文件已拷贝为: {new_name}")
        return False
    except FileNotFoundError:
        print(f"错误: 文件 {old_name} 不存在！")
        return True
    except FileExistsError:
        print(f"错误: 文件 {new_name} 已存在！")
        return True


def copy_and_add_metadata(csv_path, disc):
    print('读取文件"' + csv_path + '"...')
    with open(csv_path, mode="r", encoding="utf-8") as file:
        reader = csv.reader(file)
        words = list(reader)

        break_flag = False
        seq = 1
        for word in words:
            if len(word) != 4:
                print("输入格式错误。正确格式：")
                print("单词, 类型, 含义, 音频块编号")
                break
            new_name = "{}-{}. {}.{}".format(
                disc,
                str(seq).zfill(2),
                word[0],
                audio_type,
            )
            break_flag = copy_file(f"chunks{word[3]}.{audio_type}", new_name)
            if break_flag:
                break
            artist = word[1] + " " + word[2]
            if len(word[1]) == 0:
                artist = word[2]
            break_flag = set_mp3_metadata(
                new_name,
                word[0],
                artist,
                unit,
                seq,
                disc,
                book,
            )
            if break_flag:
                break
            seq += 1


if __name__ == "__main__":
    count = split_audio()
    print(f"共产生{count}个音频片段")
    copy_and_add_metadata(file1, disc=1)
    copy_and_add_metadata(file2, disc=2)
