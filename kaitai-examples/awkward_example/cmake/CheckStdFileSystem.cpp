#include <filesystem>
#include <iostream>

int main(){
	for(auto& f: std::fs::directory_iterator(".")){
		std::cout << f.path();
	}
	return 0;
}