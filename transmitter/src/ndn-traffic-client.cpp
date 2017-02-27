#include "ndn-traffic-client.hpp"

namespace ndn {

NdnTrafficClient::NdnTrafficClient(const char *programName)
  : m_programName(programName)
  , m_logger("NdnTrafficClient")
  , m_instanceId(to_string(std::rand()))
  , m_hasError(false)
  , m_hasQuietConsole(false)
  , m_hasLogFile(false)
  , m_interestInterval(time::milliseconds(1000))
  , m_nMaximumInterests(-1)
  , m_face(m_ioService)
  , m_scheduler(m_ioService)
  , m_nOutInterest(0)
  , m_nInData(0)
  , m_nInNack(0)
  , m_totalRtt(0.0) {
}

void NdnTrafficClient::usage() {
  std::cout << "Usage:\n"
            << "  " << m_programName << " [options]\n"
            << "\n"
            << "Generate Interest traffic as per provided Traffic Configuration File.\n"
            << "Interests are continuously generated unless a total number is specified.\n"
            << "\n"
            << "Options:\n"
            << "  [-i interval] - set interest generation interval in microseconds (default 1000)\n"
            << "  [-c count]    - set total number of interests to be generated\n"
		        << "  [-f conf]     - set traffic configuration file\n"
            << "  [-q]          - turn off console output\n"
            << "  [-l]          - print logs into logfile\n"
            << "  [-h]          - print this help text and exit\n";
  exit(EXIT_FAILURE);
}

void NdnTrafficClient::setInterestInterval(int interval) {
	m_interestInterval = time::milliseconds(interval);
}

void NdnTrafficClient::setMaximumInterests(int count) {
	m_nMaximumInterests = count;
}

void NdnTrafficClient::setQuietConsole() {
	m_hasQuietConsole = true;
}
void NdnTrafficClient::setLogFile() {
	m_hasLogFile = true;
}
void NdnTrafficClient::setConfigurationFile(const char *conf) {
	m_configurationFile = conf;
}

bool NdnTrafficClient::hasError() {
	return m_hasError;
}

void NdnTrafficClient::initializeTraffic() {
	if(boost::filesystem::exists(boost::filesystem::path(m_configurationFile))) {
		m_trafficStream.open(m_configurationFile.c_str());
	} else {
    m_logger.log("ERROR - Traffic Configuration File Does Not Exist: " + m_configurationFile);
    m_logger.shutdownLogger();
    exit(EXIT_FAILURE);
	}
}

void NdnTrafficClient::initializeLogger() {
	m_logger.initializeLog(m_instanceId);
}

void NdnTrafficClient::logStatistics() {
  m_logger.log("\n\n== Interest Traffic Report ==\n");

  m_logger.log("Total Interests Sent        = " +
    to_string(m_nOutInterest));
  m_logger.log("Total Responses Received    = " +
    to_string(m_nInData));
  m_logger.log("Total Nacks Received        = " +
    to_string(m_nInNack));

  double loss = 0;
  if (m_nOutInterest > 0)
    loss = (m_nOutInterest - m_nInData) * 100.0 / m_nOutInterest;
  m_logger.log("Total Interest Loss         = " +
  		to_string(loss) + "%");

  m_logger.log("Total Round Trip Time       = " +
    to_string(m_totalRtt) + "ms");
}

void NdnTrafficClient::signalHandler() {
  logStatistics();
  m_logger.shutdownLogger();
  m_face.shutdown();
  m_ioService.stop();

  exit(m_hasError ? EXIT_FAILURE : EXIT_SUCCESS);
}

void NdnTrafficClient::onData(const Interest& interest,
		const Data& data,
		time::steady_clock::TimePoint sentTime) {
  m_logger.log("Interest Received - Name=" + interest.getName().toUri());
	++m_nInData;
	double roundTripTime = (time::steady_clock::now() - sentTime).count() / 1000000.0;
	m_totalRtt += roundTripTime;
}

void NdnTrafficClient::onNack(const Interest& interest, const lp::Nack& nack) {
	m_logger.log("Interest Nack'd - Name=" + interest.getName().toUri() +
			", NackReason=" + to_string((int)nack.getReason()));
	++m_nInNack;
}
void NdnTrafficClient::onTimeout(const Interest& interest) {
  m_logger.log("Interest Timed Out - Name=" + interest.getName().toUri());
}

name::Component NdnTrafficClient::generateNameComponent() {
  std::string str;
  m_trafficStream >> str;
  return name::Component(str);
}

void NdnTrafficClient::sendInterest() {
	Name interestName("/ndn/");
	interestName.append(generateNameComponent());
	Interest interest(interestName);
	interest.setInterestLifetime(time::seconds(4));

  try {
  	time::steady_clock::TimePoint sentTime = time::steady_clock::now();
		m_face.expressInterest(interest,
													 bind(&NdnTrafficClient::onData, this, _1, _2, sentTime),
													 bind(&NdnTrafficClient::onNack, this, _1, _2),
													 bind(&NdnTrafficClient::onTimeout, this, _1));
		m_nOutInterest++;
    m_logger.log("Sending Interest   - GlobalID=" + to_string(m_nOutInterest) +
        ", Name=" + interest.getName().toUri());

    if(m_nMaximumInterests > 0 && m_nOutInterest >= m_nMaximumInterests) return;
    m_scheduler.scheduleEvent(m_interestInterval,
 			bind(&NdnTrafficClient::sendInterest, this));

  } catch (const std::exception& e) {
    m_logger.log("ERROR: " + std::string(e.what()));
  }
}

void NdnTrafficClient::run() {
	initializeTraffic();
	initializeLogger();

  boost::asio::signal_set signalSet(m_ioService, SIGINT, SIGTERM);
  signalSet.async_wait(bind(&NdnTrafficClient::signalHandler, this));

	m_scheduler.scheduleEvent(m_interestInterval,
			bind(&NdnTrafficClient::sendInterest, this));

	// m_ioService.run() will block until all events finished or m_ioService.stop() is called
	// m_ioService.run();

	// processEvents will block until the requested data received or timeout occurs.
	 try{
		 m_face.processEvents();
	 } catch (const std::exception& e) {
     m_logger.log("ERROR: " + std::string(e.what()));
     m_logger.shutdownLogger();
     m_hasError = true;
     m_ioService.stop();
   }
}
	
} // namespace ndn
