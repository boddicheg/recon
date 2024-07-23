import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { getProjectCommands, ProjectCommands } from "../services/Api";

interface RouteParams {
  [uuid: string]: string | undefined;
}

const Project: React.FC = () => {
  const { uuid } = useParams<RouteParams>();

  const [project, setProject] = useState<ProjectCommands>({
    name: "",
    uuid: "",
    commands: [],
  });

  const [, setLoading] = useState<boolean>(true);
  const [, setError] = useState<string | null>(null);

  const getProjectData = async (uuid: string | undefined) => {
    try {
      const data = await getProjectCommands(uuid);
      setProject(data);
    } catch (err) {
      if (err instanceof Error) {
        setError(err.message);
      } else {
        setError("An unexpected error occurred");
      }
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    getProjectData(uuid);
  }, []);

  return (
    <>
      <header className="bg-white shadow">
        <div className="flex flex-row place-content-between mx-auto max-w-7xl px-3 py-3">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">
            Projects / {uuid}
          </h2>
        </div>
      </header>
      <div>
        <ul role="list" className="flex flex-col divide-y divide-gray-100">
          {project &&
            project.commands &&
            project.commands?.map((command) => (
              <li className="flex justify-between gap-x-6 py-1 px-1 my-2 border border-slate-100 bg-slate-50 shadow-md rounded hover:shadow-lg cursor-pointer">
                <div className="flex min-w-0 gap-x-4">
                  <div className="min-w-0 content-center ">
                    icon
                  </div>
                  <div className="min-w-0 flex-auto">
                    <p className="text-lg leading-6 text-gray-900">
                      Command: <span className="font-bold">{command}</span>
                    </p>
                    <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                      Added: 123
                    </p>
                  </div>
                </div>
                <div className="inline-flex"> 
                <button>Run</button>
                <button>Cancel</button>
                </div>
              </li>
            ))}
        </ul>
      </div>
    </>
  );
};

export default Project;
