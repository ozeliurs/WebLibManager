import { useState, useEffect } from "react";

const ScansList = () => {
  const [scans, setScans] = useState([]);

  useEffect(() => {
    const fetchScans = async () => {
      const res = await fetch("https://weblibmanager.ozeliurs.com/api/scans/");
      const data = await res.json();
      setScans(data);
    };

    fetchScans();
    const interval = setInterval(fetchScans, 5000);
    return () => clearInterval(interval);
  }, []);

  return (
    <div className="overflow-x-auto">
      <table className="table">
        <thead>
          <tr>
            <th>ID</th>
            <th>Status</th>
            <th>Created At</th>
            <th>Updated At</th>
          </tr>
        </thead>
        <tbody>
          {scans.map((scan) => (
            <tr key={scan.id}>
              <td>{scan.id}</td>
              <td>
                <div
                  className="badge"
                  className={
                    scan.status === "completed"
                      ? "badge-success"
                      : scan.status === "failed"
                        ? "badge-error"
                        : "badge-warning"
                  }
                >
                  {scan.status}
                </div>
              </td>
              <td>{new Date(scan.created_at).toLocaleString()}</td>
              <td>{new Date(scan.updated_at).toLocaleString()}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default ScansList;
