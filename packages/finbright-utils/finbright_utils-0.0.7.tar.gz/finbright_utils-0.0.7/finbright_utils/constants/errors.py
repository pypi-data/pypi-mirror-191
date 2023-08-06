class LenghtNotMatch(Exception):
    def __init__(self, message="Length of Two Series Do not Match"):            
        # Call the base class constructor with the parameters it needs
        super().__init__(message)