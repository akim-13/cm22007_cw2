import { render, screen, fireEvent } from "@testing-library/react";
import SettingsModal from "../components/SettingsModal";
import "@testing-library/jest-dom";

// Mock the alert function
window.alert = jest.fn();

describe("SettingsModal", () => {
  const mockOnClose = jest.fn();

  afterEach(() => {
    jest.clearAllMocks();
  });

  test("renders correctly when open", () => {
    render(<SettingsModal open={true} onClose={mockOnClose} />);
    expect(screen.getByText("Settings")).toBeInTheDocument();
  });

  test("does not render when closed", () => {
    render(<SettingsModal open={false} onClose={mockOnClose} />);
    expect(screen.queryByText("Settings")).not.toBeInTheDocument();
  });

  test("calls onClose when cancel button is clicked", () => {
    render(<SettingsModal open={true} onClose={mockOnClose} />);
    const cancelButton = screen.getByText("Cancel");
    fireEvent.click(cancelButton);
    expect(mockOnClose).toHaveBeenCalledTimes(1);
  });
});
