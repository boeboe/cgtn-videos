
# pylint: disable=too-many-arguments
"""Package to model videos from CGTN """

class Video(object):
    """Common class to represent video objects with metadata from CGTN.

    Args:
        uid: a unique id of the video.
        channel_id: a channel id of the video.
        video_url: url to the m3u8 steaming link of the video.
        img_url: url to a cover or poster image representing the video.
        web_url: url to a news or details page belonging to the video.
        title: title or name or headline of the video.
        details: details or extended headline belonging to the video.
        editor: editor or creator of the video.
        publish_date: the date of publishing of the video.
        start_date: the starting date of the video.
        end_date: a end date of the video.
    """

    def __init__(self, uid=None, channel_id=None, video_url=None, img_url=None, web_url=None, title=None, details=None,
                 editor=None, publish_date=None, start_date=None, end_date=None):
        self.uid = uid
        self.channel_id = channel_id

        self.video_url = video_url
        self.img_url = img_url
        self.web_url = web_url

        self.title = title
        self.details = details
        self.editor = editor

        self.publish_date = publish_date
        self.start_date = start_date
        self.end_date = end_date

    def __eq__(self, other):
        """Overrides the default implementation"""
        if isinstance(other, Video):
            return self.video_url == other.video_url
        return False

    def __hash__(self):
        return hash((frozenset(self.video_url)))

    def __str__(self):
        return str(self.__class__) + ": " + str(self.__dict__)

    def __repr__(self):
        return str(self.__class__) + ": " + str(self.__dict__)
