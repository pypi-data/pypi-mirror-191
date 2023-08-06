# Deluge Interface

## Installing
```
python3 -m pip install deluge_interface
```

## Requirements
- A running Deluge service

## Usage
```python
from deluge_interface import Deluge, Torrent, TorrentStatus

deluge = Deluge("http(s)://example.deluge.com", "your_password_here")
torrent: Torrent = deluge.add_magnet(uri: str)
status: TorrentStatus = torrent.get_status()
deluge.remove_torrent(torrent.id, False)
```

### Adding Torrents
Torrents can be added by magnet link, local `.torrent` file, or a remotely hosted URL to a `.torrent` file. The relevant methods are as follows:
- `Deluge().add_magnet(uri: str, **kwargs) -> Torrent`
    Adds a magnet link to the queue, and returns a Torrent object with the relevant data.
- `Deluge().add_torrent_from_url(url: str, headers: dict[str, str] = {}, **kwargs) -> Torrent`
    Adds a torrent URL to the queue, and returns a Torrent object with the relevant data.
- `Deluge().add_torrent_from_file(*path, **kwargs) -> Torrent`
    Adds a torrent file from `path` to the queue, and returns a Torrent object with the relevant data.

### Managing Torrents
Torrents can be removed, paused, or resumed in the current library version. The relevant methods are as follows:
- `Deluge().remove_torrent(torrent_id: str, remove_data: bool = False)`
    Removes torrent with id `torrent_id`. If `remove_data` is true, all data associated with the torrent will also be removed
- `Torrent().pause()`
    Pauses the torrent object.
- `Torrent().resume()`
    Resumes the torrent object.
- `Deluge().list_torrents() -> list[Torrent]`
    Gets all active torrents.