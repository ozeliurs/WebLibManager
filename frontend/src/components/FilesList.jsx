import { useState, useEffect } from "react";

const FilesList = () => {
  const [files, setFiles] = useState([]);
  const [filters, setFilters] = useState({
    video_codec: "",
    audio_codec: "",
    subtitle_codec: "",
  });

  useEffect(() => {
    fetch("https://weblibmanager.ozeliurs.com/api/files/?limit=100000000")
      .then((res) => res.json())
      .then((data) => setFiles(data));
  }, []);

  const filteredFiles = files.filter((file) => {
    return (
      (!filters.video_codec || file.video_codec === filters.video_codec) &&
      (!filters.audio_codec || file.audio_codec === filters.audio_codec) &&
      (!filters.subtitle_codec ||
        file.subtitle_codec === filters.subtitle_codec)
    );
  });

  // Helper function to determine badge classes based on codec type and value
  const getBadgeClasses = (type, codec) => {
    const baseClasses = "badge ";

    switch (type) {
      case "video":
        return (
          baseClasses +
          (codec === "h264" ? "badge-primary" : "badge-primary badge-outline")
        );
      case "audio":
        return (
          baseClasses +
          (codec === "aac"
            ? "badge-secondary"
            : "badge-secondary badge-outline")
        );
      case "subtitle":
        return (
          baseClasses +
          (codec === "subrip" ? "badge-accent" : "badge-accent badge-outline")
        );
      default:
        return baseClasses + "badge-ghost";
    }
  };

  return (
    <div>
      <div className="flex gap-4 mb-4">
        <select
          className="select select-bordered"
          value={filters.video_codec}
          onChange={(e) =>
            setFilters({ ...filters, video_codec: e.target.value })
          }
        >
          <option value="">All Video Codecs</option>
          {[...new Set(files.map((f) => f.video_codec).filter(Boolean))].map(
            (codec) => (
              <option key={codec} value={codec}>
                {codec}
              </option>
            ),
          )}
        </select>

        <select
          className="select select-bordered"
          value={filters.audio_codec}
          onChange={(e) =>
            setFilters({ ...filters, audio_codec: e.target.value })
          }
        >
          <option value="">All Audio Codecs</option>
          {[...new Set(files.map((f) => f.audio_codec).filter(Boolean))].map(
            (codec) => (
              <option key={codec} value={codec}>
                {codec}
              </option>
            ),
          )}
        </select>

        <select
          className="select select-bordered"
          value={filters.subtitle_codec}
          onChange={(e) =>
            setFilters({ ...filters, subtitle_codec: e.target.value })
          }
        >
          <option value="">All Subtitle Codecs</option>
          {[...new Set(files.map((f) => f.subtitle_codec).filter(Boolean))].map(
            (codec) => (
              <option key={codec} value={codec}>
                {codec}
              </option>
            ),
          )}
        </select>
      </div>

      <div className="overflow-x-auto">
        <table className="table">
          <thead>
            <tr>
              <th>Path</th>
              <th>Size</th>
              <th>Video Codec</th>
              <th>Audio Codec</th>
              <th>Subtitle Codec</th>
            </tr>
          </thead>
          <tbody>
            {filteredFiles.map((file) => (
              <tr key={file.path}>
                <td>{file.path}</td>
                <td>{(file.size / 1024 / 1024).toFixed(2)} MB</td>
                <td>
                  {file.video_codec && (
                    <div className={getBadgeClasses("video", file.video_codec)}>
                      {file.video_codec}
                    </div>
                  )}
                </td>
                <td>
                  {file.audio_codec && (
                    <div className={getBadgeClasses("audio", file.audio_codec)}>
                      {file.audio_codec}
                    </div>
                  )}
                </td>
                <td>
                  {file.subtitle_codec && (
                    <div
                      className={getBadgeClasses(
                        "subtitle",
                        file.subtitle_codec,
                      )}
                    >
                      {file.subtitle_codec}
                    </div>
                  )}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FilesList;
