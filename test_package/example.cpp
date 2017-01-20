#include <OIS/OIS.h>
#include <iostream>

int main(int argc, char *argv[])
{
	std::cout << "OIS version: " << OIS::InputManager::getVersionNumber() << std::endl;
	return 0;
}