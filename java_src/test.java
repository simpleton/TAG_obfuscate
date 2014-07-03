package com.tencent.mm.plugin.report.service;

import android.util.SparseArray;

import com.tencent.mm.algorithm.MD5;
import com.tencent.mm.model.MMCore;
import com.tencent.mm.modelbase.NetSceneBase;
import com.tencent.mm.plugin.report.model.IReportInfo;
import com.tencent.mm.plugin.report.model.ReportProtocol;
import com.tencent.mm.sdk.platformtools.Log;

/* package */final class ReportLogic {

	private static final String TAG = "MicroMsg.ReportLogic";

	/* package */ static void inQueue(final IReportInfo info, final boolean sync) {

		if (info == null) {
			Log.w(TAG, "inqueue info is null");
			return;
		}

		int type = info.getType();
		final IReportHelper helper = reportHelperMap.get(type);
		if (helper != null) {
			Log.v(TAG, "get reportHelper ok, type=%d, sync=%B", type, sync);
			if (!sync) {

				MMCore.getWorkerThread().postToWorker(new Runnable() {

					@Override
					public void run() {
                                            Log.w(TAG, "hello hello hello");
						helper.doJob(info);
					}
				});
			} else {

				helper.doJob(info);
			}
		} else {
			Log.d(TAG, "get reportHelper fail, it is null, type=%d", type);
		}
	}

	/* package */ static void doSave(int type) {
		IReportHelper helper = reportHelperMap.get(type);
		if (helper != null) {
			helper.save();
		}
	}

	/* package */ static void doSaveAll() {
		// sync
		for (int i = 0; i < reportHelperMap.size(); ++i) {
			Log.v(TAG, "do save, key = %d", reportHelperMap.keyAt(i));
			reportHelperMap.valueAt(i).save();
		}
	}

	/* package */ static void doClearAll() {
		// sync
		for (int i = 0; i < reportHelperMap.size(); ++i) {
			Log.v(TAG, "do clear, key = %d", reportHelperMap.keyAt(i));
			reportHelperMap.valueAt(i).clear();
		}
	}

	/* package */ static NetSceneBase getReport(int type) {
		IReportHelper helper = reportHelperMap.get(type);
		if (helper != null) {
			return helper.getReportNetScene();
		}
		return null;
	}

	/* package */ static String getReportRuleFilePath() {
		if (MMCore.accHasReady()) {
			return String.format("%s/%s", MMCore.getAccStg().getCacheReportPath(), MD5.getMessageDigest("__report_rule__".getBytes()));
		}
		return "";
	}

	/* Package */ interface IReportHelper {

		int doJob(IReportInfo info);

		void save();

		void clear();

		NetSceneBase getReportNetScene();
	}

	private static SparseArray<ReportLogic.IReportHelper> reportHelperMap;

	static {
		/* register helper*/
		reportHelperMap = new SparseArray<ReportLogic.IReportHelper>();
		reportHelperMap.put(ReportProtocol.MM_USERACTION, new ClickStreamReportHelper());
		reportHelperMap.put(ReportProtocol.MM_KVSTAT, new KVReportHelper());
		reportHelperMap.put(ReportProtocol.MM_CLIENTPERFORMANCE, new ClientPerfReportHelper());
	}

	private ReportLogic() {
		throw new IllegalAccessError("can not call this constructor");
	}
}
