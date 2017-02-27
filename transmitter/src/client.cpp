#include "ndn-traffic-client.hpp"

int main(int argc, char* argv[]) {
  std::srand(std::time(nullptr));

  ndn::NdnTrafficClient client(argv[0]);

  bool hasConfigurationFile = false;
  char option;
  while ((option = getopt(argc, argv, "hqli:c:f:")) != -1) {
    switch (option) {
    case 'h':
      client.usage();
      break;
    case 'i':
      client.setInterestInterval(atoi(optarg));
      break;
    case 'c':
      client.setMaximumInterests(atoi(optarg));
      break;
    case 'q':
      client.setQuietConsole();
      break;
    case 'l':
      client.setLogFile();
      break;
    case 'f':
      client.setConfigurationFile(optarg);
      hasConfigurationFile = true;
      break;
    default:
      client.usage();
      break;
    }
  }

  if(!hasConfigurationFile) {
  	client.usage();
  }

  client.run();

  return client.hasError() ? EXIT_FAILURE : EXIT_SUCCESS;
}

