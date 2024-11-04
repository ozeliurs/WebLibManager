import { useState, useEffect } from "react";

const FilesList = () => {
  const [files, setFiles] = useState([]);
  const [filters, setFilters] = useState({
    video_codec: "",
    audio_codec: "",
    subtitle_codec: "",
  });

  useEffect(() => {
    fetch("https://weblibmanager.ozeliurs.com/api/files/")
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
        {/* Similar selects for audio and subtitle codecs */}
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
                <td>{file.video_codec}</td>
                <td>{file.audio_codec}</td>
                <td>{file.subtitle_codec}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
};

export default FilesList;
