#ifndef NDN_TRAFFIC_CLIENT_HPP
#define NDN_TRAFFIC_CLIENT_HPP

#include <cctype>
#include <cstdlib>
#include <fstream>
#include <string>
#include <unistd.h>

#include <boost/asio.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>
#include <boost/filesystem.hpp>
#include <boost/noncopyable.hpp>

#include <ndn-cxx/name-component.hpp>
#include <ndn-cxx/face.hpp>
#include <ndn-cxx/util/scheduler.hpp>

#include "logger.hpp"

namespace ndn {

class NdnTrafficClient: boost::noncopyable {
public:
	explicit NdnTrafficClient(const char *);

	void usage();
  void setInterestInterval(int);
  void setMaximumInterests(int);
  void setQuietConsole();
  void setLogFile();
  void setConfigurationFile(const char *);
  bool hasError();
  
  void initializeTraffic();
  void initializeLogger();
  void logStatistics();
  void signalHandler();

  void onData(const Interest&, const Data&, time::steady_clock::TimePoint);
  void onNack(const Interest&, const lp::Nack&);
  void onTimeout(const Interest&);

  name::Component generateNameComponent();
  void sendInterest();
  void run();
	
private:
  std::string m_programName;
  Logger m_logger;
  std::string m_instanceId;
  bool m_hasError;
  bool m_hasQuietConsole;
  bool m_hasLogFile;
  
  time::milliseconds m_interestInterval;
  int m_nMaximumInterests;
  std::string m_configurationFile;
  std::ifstream m_trafficStream;
  
  boost::asio::io_service m_ioService;
  Face m_face;
  Scheduler m_scheduler;

  int m_nOutInterest;
  int m_nInData;
  int m_nInNack;
  double m_totalRtt;
};
	
} // namespace ndn

#endif // NDN_TRAFFIC_CLIENT_HPP