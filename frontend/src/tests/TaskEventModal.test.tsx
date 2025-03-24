import React from "react";
import { render, screen } from "@testing-library/react";
import TaskEventModal from "../components/TaskEventModal";
import "@testing-library/jest-dom";

// Mock the TaskEventInputs components
jest.mock("../components/TaskEventInputs", () => ({
  TitleInput: ({ value, onChange }: any) => (
    <input data-testid="title-input" value={value} onChange={onChange} />
  ),
  StartDateInput: ({ value, onChange }: any) => (
    <input data-testid="start-date-input" value={value} onChange={onChange} />
  ),
  EndDateInput: ({ value, onChange }: any) => (
    <input data-testid="end-date-input" value={value} onChange={onChange} />
  ),
  DurationInput: ({ value, onChange }: any) => (
    <input data-testid="duration-input" value={value} onChange={onChange} />
  ),
  PrioritySelect: ({ value, onChange }: any) => (
    <select data-testid="priority-select" value={value} onChange={onChange}>
      <option value="1">Low Priority</option>
      <option value="2">Medium Priority</option>
      <option value="3">High Priority</option>
    </select>
  ),
  DescriptionInput: ({ value, onChange }: any) => (
    <textarea data-testid="description-input" value={value} onChange={onChange} />
  ),
  CompletedCheckbox: ({ checked, onChange }: any) => (
    <input type="checkbox" data-testid="completed-checkbox" checked={checked} onChange={onChange} />
  ),
  ModeToggleButton: ({ mode, isActive }: any) => (
    <button data-testid={`${mode}-toggle`}>{mode}</button>
  ),
}));

// Mock axios
jest.mock("axios", () => ({
  put: jest.fn(() => Promise.resolve({ data: {} })),
  post: jest.fn(() => Promise.resolve({ data: {} })),
  delete: jest.fn(() => Promise.resolve({ data: {} })),
  get: jest.fn(() => Promise.resolve({ data: {} })),
}));

describe("TaskEventModal", () => {
  const defaultProps = {
    events: [],
    setEvents: jest.fn(),
    isModalOpen: true,
    setIsModalOpen: jest.fn(),
    newFCEvent: { 
      current: {
        title: "",
        start: "",
        end: "",
        extendedProps: {
          description: "",
          duration: "",
          priority: "",
          isCompleted: false
        }
      }
    },
    initialExtendedProps: {},
    isTaskMode: true,
    setIsTaskMode: jest.fn()
  };

  beforeEach(() => {
    jest.clearAllMocks();
  });

  test("renders modal title for task mode", () => {
    render(<TaskEventModal {...defaultProps} />);
    expect(screen.getByText(/Manage Task/i)).toBeInTheDocument();
  });

  test("renders modal title for event mode", () => {
    render(<TaskEventModal {...defaultProps} isTaskMode={false} />);
    expect(screen.getByText(/Manage Event/i)).toBeInTheDocument();
  });

  test("does not render when modal is closed", () => {
    render(<TaskEventModal {...defaultProps} isModalOpen={false} />);
    expect(screen.queryByText(/Manage Task/i)).not.toBeInTheDocument();
  });

  test("renders task mode inputs", () => {
    render(<TaskEventModal {...defaultProps} />);
    expect(screen.getByTestId("title-input")).toBeInTheDocument();
    expect(screen.getByTestId("start-date-input")).toBeInTheDocument();
    expect(screen.getByTestId("duration-input")).toBeInTheDocument();
    expect(screen.getByTestId("priority-select")).toBeInTheDocument();
    expect(screen.getByTestId("description-input")).toBeInTheDocument();
    expect(screen.getByTestId("completed-checkbox")).toBeInTheDocument();
  });

  test("renders event mode inputs", () => {
    render(<TaskEventModal {...defaultProps} isTaskMode={false} />);
    expect(screen.getByTestId("title-input")).toBeInTheDocument();
    expect(screen.getByTestId("start-date-input")).toBeInTheDocument();
    expect(screen.getByTestId("end-date-input")).toBeInTheDocument();
    expect(screen.getByTestId("description-input")).toBeInTheDocument();
  });
});
