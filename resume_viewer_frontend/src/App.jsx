import React, { useState } from "react";
import './index.css';

export default function App() {
  const [pdfFile, setPdfFile] = useState(null);
  const [resumeData, setResumeData] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!pdfFile) return;
    const formData = new FormData();
    formData.append("file", pdfFile);

    setLoading(true);
    const res = await fetch("http://localhost:8000/parse-resume/", {
      method: "POST",
      body: formData,
    });

    const result = await res.json();
    setResumeData(JSON.parse(result.parsed_output));
    setLoading(false);
  };

  return (
    <div className="min-h-screen bg-gray-50 p-6 font-sans">
      <div className="max-w-4xl mx-auto">
        <div className="mb-6 flex items-center gap-4">
          <input
            type="file"
            accept="application/pdf"
            onChange={(e) => setPdfFile(e.target.files[0])}
          />
          <button
            onClick={handleUpload}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            {loading ? "Parsing..." : "Upload & Parse"}
          </button>
        </div>

        {resumeData && (
          <div className="bg-white shadow-md rounded-lg p-6 space-y-6">
            <div>
              <h1 className="text-2xl font-bold">{resumeData.name}</h1>
              <p className="text-gray-600">{resumeData.email}</p>
              {resumeData.miscellaneous?.map((item, i) => (
                <p className="text-sm text-gray-500" key={i}>{item}</p>
              ))}
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-2">Skills</h2>
              <div className="flex flex-wrap gap-2">
                {resumeData.skills.map((skill, i) => (
                  <span
                    key={i}
                    className="px-3 py-1 text-sm bg-gray-200 rounded-full"
                  >
                    {skill}
                  </span>
                ))}
              </div>
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-2">Experience</h2>
              {resumeData.experience.map((exp, i) => (
                <div key={i} className="mb-4">
                  <h3 className="font-semibold">{exp.title} – {exp.company}</h3>
                  <p className="text-sm text-gray-500">{exp.duration} | {exp.location}</p>
                  <ul className="list-disc list-inside">
                    {exp.highlights.map((pt, j) => (
                      <li key={j}>{pt}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-2">Education</h2>
              {resumeData.education.map((edu, i) => (
                <div key={i} className="mb-2">
                  <p className="font-semibold">{edu.degree}</p>
                  <p className="text-sm text-gray-600">{edu.university}</p>
                  <p className="text-sm text-gray-500">{edu.duration} | {edu.location}</p>
                </div>
              ))}
            </div>

            <div>
              <h2 className="text-xl font-semibold mb-2">Projects</h2>
              {resumeData.projects.map((proj, i) => (
                <div key={i} className="mb-2">
                  <p className="font-semibold">{proj.name}</p>
                  <ul className="list-disc list-inside">
                    {proj.highlights.map((pt, j) => (
                      <li key={j}>{pt}</li>
                    ))}
                  </ul>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}