import React, { useEffect, useState } from "react";
import moment from 'moment';
import { useNavigate } from 'react-router-dom';

import AddProjectModal from './AddProjectModal';
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
            className="flex justify-between gap-x-6 py-3 px-3 my-4 border border-slate-100 bg-slate-50 shadow-md rounded hover:shadow-lg cursor-pointer">
            <div className="flex min-w-0 gap-x-4">
              <div className="min-w-0 content-center ">
                <svg
                  xmlns="http://www.w3.org/2000/svg"
                  fill="none"
                  viewBox="0 0 24 24"
                  strokeWidth={1.5}
                  stroke="currentColor"
                  className="size-8 fill-indigo-500 stroke-indigo-700"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    d="m9 13.5 3 3m0 0 3-3m-3 3v-6m1.06-4.19-2.12-2.12a1.5 1.5 0 0 0-1.061-.44H4.5A2.25 2.25 0 0 0 2.25 6v12a2.25 2.25 0 0 0 2.25 2.25h15A2.25 2.25 0 0 0 21.75 18V9a2.25 2.25 0 0 0-2.25-2.25h-5.379a1.5 1.5 0 0 1-1.06-.44Z"
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
    console.log(message)
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
