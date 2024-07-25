import React, { useEffect, useState } from "react";
import moment from "moment";
import { useNavigate } from "react-router-dom";

import AddProjectModal from "./AddProjectModal";
import { fetchProjects, ProjectsInterface } from "../services/Api";

export const ProjectsList = ({
  projects,
}: {
  projects?: Array<ProjectsInterface>;
}) => {
  const navigate = useNavigate();

  const navigateTo = (uuid: string) => {
    navigate(`/project/${uuid}`);
  };

  return (
    <div>
      {projects &&
        projects?.map((project) => (
          <li
            onClick={() => navigateTo(project.uuid)}
            className="flex justify-between gap-x-6 py-3 px-3 my-4 border border-slate-100 bg-slate-50 shadow-md rounded hover:shadow-lg cursor-pointer"
          >
            <div className="flex min-w-0 gap-x-4">
              <div className="min-w-0 content-center ">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="size-8 stroke-indigo-700"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="M12 21a9.004 9.004 0 0 0 8.716-6.747M12 21a9.004 9.004 0 0 1-8.716-6.747M12 21c2.485 0 4.5-4.03 4.5-9S14.485 3 12 3m0 18c-2.485 0-4.5-4.03-4.5-9S9.515 3 12 3m0 0a8.997 8.997 0 0 1 7.843 4.582M12 3a8.997 8.997 0 0 0-7.843 4.582m15.686 0A11.953 11.953 0 0 1 12 10.5c-2.998 0-5.74-1.1-7.843-2.918m15.686 0A8.959 8.959 0 0 1 21 12c0 .778-.099 1.533-.284 2.253m0 0A17.919 17.919 0 0 1 12 16.5c-3.162 0-6.133-.815-8.716-2.247m0 0A9.015 9.015 0 0 1 3 12c0-1.605.42-3.113 1.157-4.418"
                  />
                </svg>
              </div>
              <div className="min-w-0 flex-auto">
                <p className="text-lg font-bold leading-6 text-gray-900">
                  {project?.name} / {project?.target}
                </p>
                <p className="mt-1 truncate text-xs leading-5 text-gray-500">
                  {project?.description}
                </p>
              </div>
            </div>
            <div className="inline-flex">
              <div className="hidden shrink-0 sm:flex sm:flex-col sm:items-end inline-flex">
                <p className="text-sm leading-6 text-gray-900">
                  Commands: {project?.resources}
                </p>
                <p className="mt-1 text-xs leading-5 text-gray-500">
                  Updated: {moment(project?.date_updated).fromNow()}
                </p>
              </div>
              <div className="max-w-24 content-center ml-4">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="size-8 stroke-indigo-700"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="m8.25 4.5 7.5 7.5-7.5 7.5"
                  />
                </svg>
              </div>
            </div>
          </li>
        ))}
    </div>
  );
};

const Projects: React.FC = () => {
  const [projects, setProjects] = useState<Array<ProjectsInterface>>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const getProjects = async () => {
    try {
      const data = await fetchProjects();
      setProjects(data);
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

  const onAddProject = (message: string) => {
    console.log(message);
    getProjects();
  };

  useEffect(() => {
    getProjects();
  }, []);

  if (loading) {
    return <p>Loading...</p>;
  }

  if (error) {
    return <p>Error: {error}</p>;
  }

  return (
    <>
      <header className="bg-white shadow">
        <div className="flex flex-row place-content-between mx-auto max-w-7xl px-3 py-3">
          <h2 className="text-2xl font-bold tracking-tight text-gray-900">
            Projects
          </h2>
          <span className="sm:ml-3">
            <AddProjectModal onAddProject={onAddProject} />
          </span>
        </div>
      </header>
      <div>
        <ul role="list" className="flex flex-col divide-y divide-gray-100">
          <ProjectsList projects={projects} />
        </ul>
      </div>
    </>
  );
};

export default Projects;
