import FilesystemBrowser from "../components/FilesystemBrowser";

const Home = () => {
  const handlePathSelect = async (path) => {
    try {
      const res = await fetch("https://weblibmanager.ozeliurs.com/api/scans/", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ path }),
      });
      if (res.ok) {
        window.location.href = "/scans";
      }
    } catch (error) {
      console.error("Failed to start scan:", error);
    }
  };

  return (
    <div className="container mx-auto p-4">
      <h1 className="text-2xl font-bold mb-4">Start New Scan</h1>
      <FilesystemBrowser onSelectPath={handlePathSelect} />
    </div>
  );
};

export default Home;
